import json
import math
import re
from datetime import datetime

_CSE_POST_TIMEOUT = (10, 30)


def _as_float(value):
    """Return a finite float for *value*, or None when it cannot be trusted."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        text = value.strip().replace(",", "").replace("%", "").replace("\u2212", "-")
        if not text or text in ("--", "-"):
            return None
        try:
            number = float(text)
        except ValueError:
            return None
    else:
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def _as_int(value):
    number = _as_float(value)
    if number is None:
        return None
    return int(number)


def parse_index_data(payload):
    """Parse the official DSE /api/live/market payload into the legacy shape."""
    if not isinstance(payload, dict):
        raise ValueError("DSE index payload is not a JSON object")

    indices = []
    rejected = 0

    totals = payload.get("totals") if isinstance(payload.get("totals"), dict) else {}
    trade_time = totals.get("tradeTime")
    if trade_time:
        indices.append({"last_update": str(trade_time)})

    rows = payload.get("indices") if isinstance(payload.get("indices"), list) else []
    count = 0
    for row in rows:
        if count >= 3:
            break
        if not isinstance(row, dict):
            rejected += 1
            continue
        name = row.get("key")
        value = _as_float(row.get("value"))
        change = _as_float(row.get("change"))
        percent = _as_float(row.get("percent"))
        if not name or value is None or change is None or percent is None:
            rejected += 1
            continue
        if change > 0:
            arrow = "upArrow"
        elif change < 0:
            arrow = "downArrow"
        else:
            arrow = ""
        indices.append({
            "index": str(name),
            "value": value,
            "change": change,
            "percent": percent,
            "arrow": arrow,
        })
        count += 1

    trades = _as_float(totals.get("trades"))
    volume = _as_float(totals.get("volume"))
    turnover = _as_float(totals.get("turnover"))
    if trades is not None and volume is not None and turnover is not None:
        indices.append({
            "total_trade": int(trades),
            "total_volume": int(volume),
            "total_value": turnover,
        })

    breadth = payload.get("breadth") if isinstance(payload.get("breadth"), dict) else {}
    advanced = _as_int(breadth.get("advanced"))
    declined = _as_int(breadth.get("declined"))
    unchanged = _as_int(breadth.get("unchanged"))
    if advanced is not None and declined is not None and unchanged is not None:
        indices.append({
            "issues_advanced": advanced,
            "issues_declined": declined,
            "issues_unchanged": unchanged,
        })

    if rejected:
        print("[parse_index_data] rejected %s malformed index rows" % rejected)
    if count == 0:
        raise ValueError("No valid DSE index rows in payload")
    return indices


def parse_ticker_data(soup):
    """Parse the SSR ticker tape (div.ticker-track) of the official DSE homepage."""
    if soup is None:
        raise ValueError("DSE homepage soup is missing")

    tracks = soup.find_all("div", class_=lambda c: c and "ticker-track" in c.split())
    if not tracks:
        raise ValueError("DSE ticker track not found on homepage")

    stocks = []
    seen = set()
    rejected = 0
    for anchor in tracks[0].find_all("a", href=True):
        href = anchor.get("href") or ""
        if not href.startswith("/company/"):
            continue
        spans = anchor.find_all("span")
        if len(spans) < 6:
            rejected += 1
            continue
        inst = href.rsplit("/", 1)[-1].strip()
        price = _as_float(spans[1].get_text(strip=True))
        change = _as_float(spans[4].get_text(strip=True))
        percent = _as_float(spans[5].get_text(strip=True))
        if not inst or price is None or change is None or percent is None:
            rejected += 1
            continue
        if inst in seen:
            continue
        seen.add(inst)
        style = spans[2].get("style") or ""
        if "--up" in style:
            arrow = "tkup"
        elif "--down" in style:
            arrow = "tkdown"
        else:
            arrow = ""
        stocks.append({
            "inst": inst,
            "price": "%.2f" % price,
            "change": "%.2f" % change,
            "percent": "%.2f" % percent,
            "arrow": arrow,
        })

    if rejected:
        print("[parse_ticker_data] rejected %s malformed ticker entries" % rejected)
    if not stocks:
        raise ValueError("No ticker records parsed from DSE homepage")
    return stocks


def parse_minute_index(payload):
    """Parse minute index series from /api/live/index-intraday responses.

    *payload* maps index code (DSEX/DS30/DSES) to the decoded JSON response.
    CDSET is no longer published by the official website and is omitted.
    """
    if not isinstance(payload, dict):
        raise ValueError("DSE minute index payload is not a mapping")

    json_index = {}
    rejected = 0
    for name in ("DSEX", "DS30", "DSES"):
        response = payload.get(name)
        if not isinstance(response, dict):
            continue
        points = response.get("points") if isinstance(response.get("points"), list) else []
        series = []
        for point in points:
            if not isinstance(point, dict):
                rejected += 1
                continue
            time_text = point.get("t")
            value = _as_float(point.get("value"))
            if time_text is None or value is None:
                rejected += 1
                continue
            series.append({"time": str(time_text), "index": str(value)})
        if series:
            json_index[name] = series

    if rejected:
        print("[parse_minute_index] rejected %s malformed points" % rejected)
    if not json_index:
        raise ValueError("No DSE minute index series available")
    return json_index


def _parse_price_rows(payload, board):
    if not isinstance(payload, dict):
        raise ValueError("DSE share price payload is not a JSON object")
    cols = payload.get("cols") if isinstance(payload.get("cols"), list) else None
    rows = payload.get("rows") if isinstance(payload.get("rows"), list) else None
    if cols is None or rows is None:
        raise ValueError("DSE share price payload missing cols/rows")

    index_of = {col: i for i, col in enumerate(cols)}
    required = ("code", "ltp", "high", "low", "close", "ycp", "trades", "value", "volume", "board")
    missing = [col for col in required if col not in index_of]
    if missing:
        raise ValueError("DSE share price payload missing columns: %s" % missing)

    prices = []
    rejected = 0
    serial = 0
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) < len(cols):
            rejected += 1
            continue
        if row[index_of["board"]] != board:
            continue
        symbol = row[index_of["code"]]
        ltp = _as_float(row[index_of["ltp"]])
        high = _as_float(row[index_of["high"]])
        low = _as_float(row[index_of["low"]])
        close = _as_float(row[index_of["close"]])
        ycp = _as_float(row[index_of["ycp"]])
        trades = _as_int(row[index_of["trades"]])
        value = _as_float(row[index_of["value"]])
        volume = _as_int(row[index_of["volume"]])
        if (not isinstance(symbol, str) or not symbol.strip()
                or None in (ltp, high, low, close, ycp)
                or trades is None or value is None or volume is None):
            rejected += 1
            continue
        serial += 1
        # Legacy contract: CHANGE = (LTP - YCP); non-traded rows (LTP rendered
        # "--" on the legacy site, 0 in the new feed) report change 0.
        change_val = 0.0 if ltp == 0 else round(ltp - ycp, 2)
        prices.append({
            "sl": serial,
            "symbol": symbol.strip(),
            "ltp": round(ltp, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "closep": round(close, 2),
            "ycp": round(ycp, 2),
            "change_val": change_val,
            "trade_count": trades,
            "value_mn": round(value, 3),
            "volume": volume,
        })

    if rejected:
        print("[parse_latest_share_price] rejected %s malformed rows" % rejected)
    return prices


def parse_latest_share_price(payload):
    """Public board (board=PUBLIC) latest share prices wrapped as {"DSE": rows}."""
    prices = _parse_price_rows(payload, board="PUBLIC")
    if not prices:
        raise ValueError("No DSE public-board share price rows")
    return {"DSE": prices}

def parse_latest_share_price_debt(payload):
    """Debt board (board=DEBT) prices — the legacy 'treasury bond' page was in
    fact the DSE Debt Board (corporate bonds/debentures), verified via archive."""
    prices = _parse_price_rows(payload, board="DEBT")
    if not prices:
        raise ValueError("No DSE debt-board rows")
    return prices

# Official /api/live/prices sector labels -> (legacy DSE industry no., legacy sector name).
# IDs and names are the ones the application has always stored (verified from the
# existing api_sector_inst mapping). Sectors that never existed in the legacy set
# (Debenture, Misc, TravelLeisur) are intentionally excluded.
_DSE_SECTORS = {
    11: ("Bank", "Bank"),
    12: ("MutFund", "Mutual Funds"),
    13: ("Engineering", "Engineering"),
    14: ("FoodAllied", "Food & Allied"),
    15: ("FuelPower", "Fuel & Power"),
    16: ("Jute", "Jute"),
    17: ("Textile", "Textile"),
    18: ("PharmaChem", "Pharmaceuticals & Chemicals"),
    19: ("PaperPrint", "Paper & Printing"),
    20: ("ServRealEst", "Services & Real Estate"),
    21: ("Cement", "Cement"),
    22: ("IT", "IT Sector"),
    23: ("Tannery", "Tannery Industries"),
    24: ("Ceramic", "Ceramics Sector"),
    25: ("Insurance", "Insurance"),
    26: ("CorpBond", "Corporate Bond"),
    27: ("Telecom", "Telecommunication"),
    28: ("Financial In", "Financial Institutions"),
    88: ("TBond", "G-SEC (T.Bond)"),
}


def parse_sector_wise_inst(sector_id, payload):
    mapping = _DSE_SECTORS.get(sector_id)
    if mapping is None:
        raise ValueError("Unknown DSE sector id: %s" % sector_id)
    label, sector_name = mapping

    if not isinstance(payload, dict):
        raise ValueError("DSE share price payload is not a JSON object")
    cols = payload.get("cols") if isinstance(payload.get("cols"), list) else None
    rows = payload.get("rows") if isinstance(payload.get("rows"), list) else None
    if cols is None or rows is None:
        raise ValueError("DSE share price payload missing cols/rows")
    if "code" not in cols or "sector" not in cols:
        raise ValueError("DSE share price payload missing code/sector columns")

    code_i = cols.index("code")
    sector_i = cols.index("sector")
    symbols = []
    rejected = 0
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) < len(cols):
            rejected += 1
            continue
        if row[sector_i] != label:
            continue
        code = row[code_i]
        if isinstance(code, str) and code.strip():
            symbols.append(code.strip())
        else:
            rejected += 1

    if rejected:
        print("[parse_sector_wise_inst] rejected %s malformed rows" % rejected)
    return {
        'sector_id': sector_id,
        'sector': sector_name,
        'symbols': symbols
    }


def parse_ipo_offer(soup):
    """Extract IPO Center documents from the RSC payload of https://www.dse.com.bd/ipo."""
    if soup is None:
        raise ValueError("IPO page soup is missing")

    joined = ""
    for script in soup.find_all("script"):
        text = script.string or script.get_text() or ""
        if "self.__next_f.push" not in text:
            continue
        match = re.search(r'self\.__next_f\.push\(\[1,\s*"((?:[^"\\]|\\.)*)"\]\)', text)
        if not match:
            continue
        try:
            joined += json.loads('"' + match.group(1) + '"')
        except ValueError:
            continue

    marker = '"files"'
    marker_at = joined.find(marker)
    if marker_at == -1:
        raise ValueError("IPO files payload not found in IPO Center page")
    try:
        start = joined.index(":", marker_at) + 1
        files, _ = json.JSONDecoder().raw_decode(joined, start)
    except ValueError as exc:
        raise ValueError("Unable to decode IPO files payload: %s" % exc)

    circulars = files.get("circulars") if isinstance(files, dict) else None
    if not isinstance(circulars, list):
        raise ValueError("IPO circulars missing from payload")

    data = []
    seen = set()
    rejected = 0
    for group in circulars:
        documents = group.get("documents") if isinstance(group, dict) else None
        if not isinstance(documents, list):
            continue
        for doc in documents:
            if not isinstance(doc, dict):
                rejected += 1
                continue
            title = doc.get("title")
            href = doc.get("href")
            if (not isinstance(title, str) or not title.strip()
                    or not isinstance(href, str) or not href.strip()):
                rejected += 1
                continue
            # Titles look like "Company Name — Prospectus"; the DB stores company only.
            company = title.split("\u2014")[0].strip() or title.strip()
            if len(company) > 50:
                # api_ipo_offer.company is VARCHAR(50); skip rather than corrupt.
                rejected += 1
                continue
            # Store the path relative to the DSE host: the column is VARCHAR(100)
            # (longest path is 98 chars; an absolute URL would exceed it and drop
            # documents), and the frontend prefixes the host itself. dsebd.org
            # 301-redirects to www.dse.com.bd with the path preserved.
            if href.startswith("http://") or href.startswith("https://"):
                path = re.sub(r"^https?://[^/]+", "", href)
            else:
                path = href
            if not path.startswith("/"):
                path = "/" + path
            if len(path) > 100:
                rejected += 1
                continue
            key = (company, path)
            if key in seen:
                continue
            seen.add(key)
            data.append({"company": company, "href": path})

    if rejected:
        print("[parse_ipo_offer] rejected %s records (missing fields or column length limits)" % rejected)
    if not data:
        raise ValueError("No IPO records parsed from IPO Center page")
    return data


def parse_dse_news(payload):
    """Parse /api/live/news rows into the legacy news record shape."""
    if not isinstance(payload, dict):
        raise ValueError("DSE news payload is not a JSON object")
    rows = payload.get("rows") if isinstance(payload.get("rows"), list) else None
    if rows is None:
        raise ValueError("DSE news payload missing rows")

    data = []
    seen = set()
    rejected = 0
    for row in rows:
        if not isinstance(row, dict):
            rejected += 1
            continue
        row_id = row.get("id")
        code = row.get("code")
        summary = row.get("summary")
        body = row.get("body")
        filed_at = row.get("filedAt")
        time_text = row.get("time")

        code_text = code.strip() if isinstance(code, str) else ""
        if (not isinstance(summary, str) or not summary.strip()
                or not isinstance(body, str) or not body.strip()
                or len(summary.strip()) > 100 or len(body.strip()) > 1000
                or len(code_text) > 50):
            rejected += 1
            continue
        if not isinstance(filed_at, str) or not isinstance(time_text, str):
            rejected += 1
            continue
        publish_date = "%s %s" % (filed_at.strip(), time_text.strip())
        try:
            datetime.strptime(publish_date, "%Y-%m-%d %H:%M")
        except ValueError:
            rejected += 1
            continue
        if row_id is not None:
            if row_id in seen:
                continue
            seen.add(row_id)
        data.append({
            "Trading Code:": code_text,
            "News Title:": summary.strip(),
            "News:": body.strip(),
            "Post Date:": publish_date,
        })

    if rejected:
        print("[parse_dse_news] rejected %s malformed news rows" % rejected)
    if not data:
        raise ValueError("No DSE news records parsed")
    return data

#========================CSE========================================#
def parse_index_summary_cse(soup,post_url,csrf_token,session):
    trade = {}
    issue = {}
    all_data = []
    count = 1 
    for div in  soup.find_all("div",class_="tradesummary-right"):
        if count ==1:
            value = div.find("div",class_="value1").get_text().replace(',','')
            trade['total_value'] = round(float(value)/1000000,3)
        if count ==2:
            trade['total_trade'] = div.find("div",class_="value1").get_text()
        count = count + 1
    count = 1
    all_data.append(trade)
    arr = []
    for div in  soup.find_all("div",class_="tradesummary-left"):
        if count == 2:
            trade['total_volume'] = div.find("div",class_="value1").get_text().replace(',','')
        if count == 1:
            indicators = div.find("div",class_="value1").get_text()
            arr =  indicators.split()
            issue["issues_advanced"] = arr[1]
            issue["issues_declined"] = arr[3]
            issue["issues_unchanged"] = arr[5]
        count = count + 1
    all_data.append(issue)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.cse.com.bd",
        "Referer": "https://www.cse.com.bd/",
    }
    # CSE50
    data = {"selected_index": "CSE50", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()
    data['index'] = 'CSE50' 
    all_data.append(data)
    # CSE30
    data = {"selected_index": "CSE30", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()
    data['index'] = 'CSE30' 
    all_data.append(data)
    # CSCX
    data = {"selected_index": "CSCX", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()
    data['index'] = 'CSCX' 
    all_data.append(data)
    # CASPI
    data = {"selected_index": "CASPI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()
    data['index'] = 'CASPI' 
    all_data.append(data)
    # CSI
    data = {"selected_index": "CSI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()
    data['index'] = 'CSI' 
    all_data.append(data)

    return all_data


def parse_minute_index_cse(post_url,csrf_token,session):

    idx_data = []
    idx_title = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://www.cse.com.bd",
        "Referer": "https://www.cse.com.bd/",
    }
    # CSE50
    data = {"selected_index": "CSE50", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSE50'] = idx_data

    # CSE30
    data = {"selected_index": "CSE30", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSE30'] = idx_data

    # CSCX
    data = {"selected_index": "CSCX", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSCX'] = idx_data

    # CASPI
    data = {"selected_index": "CASPI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CASPI'] = idx_data

    # CSI
    data = {"selected_index": "CSI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data, timeout=_CSE_POST_TIMEOUT)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSI'] = idx_data

    return idx_title

def parse_latest_share_price_cse(soup):
    prices = []
    count = 1 
    mkt_prices={}
    table = soup.find('table',class_='row-border')
    keys = ["sl", "symbol", "ltp", "open","high", "low", "ycp","change_val","trade_count", "value_mn", "volume"]
    for tr in table.find_all("tr"):
        rows = []
        for td in tr.find_all("td"):
            rows.append(td.get_text(strip=True).replace(',','').replace('--','0'))
        if count > 1:
            prices.append(rows)
        count = count + 1
    json_data = []
    for row in prices:
        # make sure there are at least 7 elements (up to ycp)
        if len(row) >= 7:
            try:
                ltp = float(row[2])
                ycp = float(row[6])
                change_val = round(ltp - ycp, 2)
            except ValueError:
                change_val = 0.0
            # insert change_val after ycp
            row.insert(7, str(change_val))
        json_data.append(dict(zip(keys, row)))
        mkt_prices["CSE"]=json_data


    return mkt_prices

def parse_cse_news(soup):
    news_items = []
    for div in soup.find_all("div", class_="news_content"):
        strong = div.find("strong")
        # The page also renders helper divs (e.g. "Show all news") with the same
        # class but no <strong>; skip them instead of crashing.
        if strong is None:
            continue
        paragraphs = div.find_all("p")
        if len(paragraphs) < 2:
            continue
        title = strong.get_text(strip=True)
        content = paragraphs[1].get_text(strip=False)

        content_parts = content.split(':', 1)  # split only once
        title_parts = title.split(':', 1)

        trading_code = content_parts[0].strip() if len(content_parts[0].strip())<20 else ""
        news_body = content_parts[1].strip() if len(content_parts) > 1 else ""

        post_date = title_parts[0].strip()
        news_title = title_parts[1].strip() if len(title_parts) > 1 else ""

        news_items.append({
            "Trading Code:": trading_code,
            "News Title:": news_title,
            "News:": news_body,
            "Post Date:": post_date
        })
    return (news_items)


def parse_ticker_data_cse(soup):
    stocks = []
    for td in soup.find_all("td", class_="priceticker"):
        # Symbol
        symbol_tag = td.find("a", class_="ticker-link")
        symbol = symbol_tag.text.strip() if symbol_tag else None

        # Price
        price_tag = td.find("td", class_="trdPrice")
        price = price_tag.text.strip() if price_tag else None

        # Change and percent
        all_fonts = td.find_all("font")
        change = all_fonts[2].text.strip() if len(all_fonts) > 2 else None
        percent = all_fonts[3].text.strip() if len(all_fonts) > 3 else None

        # Arrow direction — look for next <img> after this td
        arrow_tag = td.find_next_sibling("td").find("img") if td.find_next_sibling("td") else None
        arrow_raw = arrow_tag["alt"] if arrow_tag and "alt" in arrow_tag.attrs else None
        # Normalize arrow values
        arrow_map = {
            "UP": "tkup",
            "DOWN": "tkdown",
            "NO.CHNG": "tkupdown"
        }
        arrow = arrow_map.get(arrow_raw, "tkupdown")
        stocks.append({
            "inst": symbol,
            "price": price,
            "change": change,
            "percent": percent.replace('%','') if percent is not None else percent,
            "arrow": arrow,
        })
    return stocks
