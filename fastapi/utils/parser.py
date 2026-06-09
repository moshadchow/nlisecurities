def parse_index_data(soup):
    indices = []

    last_update = soup.find("h2", class_="Bodyheading").get_text(strip=True)
    indices.append({"last_update": last_update})

    count = 1
    for row in soup.find_all("div", class_="midrow"):
        cols = row.find_all("div")
        if len(cols) == 5 and count < 4:
            indices.append({
                "index": cols[0].get_text(strip=True),
                "value": cols[1].get_text(strip=True),
                "change": cols[2].get_text(strip=True),
                "percent": cols[3].get_text(strip=True).replace('%',''),
                "arrow": cols[4].find("img")["src"].split("/")[2].split(".")[0] if cols[4].find("img") else None
            })
            count += 1

    trade_info = soup.find_all("div", class_="mol_col-wid-cus")[1]
    trade_values = [div.get_text(strip=True) for div in trade_info.find_all("div", class_="colorlight")]
    if len(trade_values) == 3:
        indices.append({
            "total_trade": trade_values[0],
            "total_volume": trade_values[1],
            "total_value": trade_values[2]
        })

    issue_info = soup.find_all("div", class_="mol_col-wid-cus")[-1]
    issue_values = [div.get_text(strip=True) for div in issue_info.find_all("div", class_="colorlight")]
    if len(issue_values) == 3:
        indices.append({
            "issues_advanced": issue_values[0],
            "issues_declined": issue_values[1],
            "issues_unchanged": issue_values[2]
        })

    return indices


def parse_ticker_data(soup):
    stocks = []

    for a in soup.find_all("a", class_="abhead"):
        text = a.get_text(" ", strip=True).replace("\xa0", " ")
        parts = text.split()

        # Expected: [inst, price, change, percent]
        if len(parts) < 4:
            continue

        img_tag = a.find("img")
        arrow = ""
        if img_tag:
            arrow = img_tag["src"].split("/")[-1].split(".")[0]

        inst = parts[0]
        price = parts[1]
        change = parts[2]
        percent = parts[3].replace("%", "")

        stocks.append({
            "inst": inst,
            "price": price,
            "change": change,
            "percent": percent,
            "arrow": arrow
        })

    return stocks

def parse_minute_index(soup):
    json_index={}
    scripts = soup.find_all("script", {"type": "text/javascript"})

    for script in scripts:
        text = script.text
        if "index_value_dsbi" in text:
            indexs = []
            start_index = text.find("var index_value_dsbi")
            end_index = text.find("var index_value_dses")
            if start_index != -1 and end_index != -1:
                chunk = text[start_index:end_index].strip()
                rows = chunk.split('=')[1].split('+')
                for row in rows:
                    col = row.split(',')
                    indexs.append(
                    {
                        "time": col[0].replace('"', '').strip()[11:],
                        "index": col[1].replace('\\n"', '').replace(';', '').strip()
                    })
            json_index['DSEX']=indexs

        if "index_value_dses" in text:
            indexs = []
            start_index = text.find("index_value_dses")
            end_index = text.find("var index_value_ds30")
            if start_index != -1 and end_index != -1:
                chunk = text[start_index:end_index].strip()
                rows = chunk.split('=')[1].split('+')
                for row in rows:
                    col = row.split(',')
                    indexs.append(
                    {
                        "time": col[0].replace('"', '').strip()[11:],
                        "index": col[1].replace('\\n"', '').replace(';', '').strip()
                    })
            json_index['DSES']=indexs

        if "index_value_ds30" in text:
            indexs = []
            start_index = text.find("var index_value_ds30")
            end_index = text.find("var index_value_cdset")
            if start_index != -1 and end_index != -1:
                chunk = text[start_index:end_index].strip()
                rows = chunk.split('=')[1].split('+')
                for row in rows:
                    col = row.split(',')
                    indexs.append(
                    {
                        "time": col[0].replace('"', '').strip()[11:],
                        "index": col[1].replace('\\n"', '').replace(';', '').strip()
                    })
            json_index['DS30']=indexs

        if "index_value_cdset" in text:
            indexs = []
            start_index = text.find("var index_value_cdset")
            end_index = text.find("var index_value_dsmex")
            if start_index != -1 and end_index != -1:
                chunk = text[start_index:end_index].strip()
                rows = chunk.split('=')[1].split('+')
                for row in rows:
                    col = row.split(',')
                    indexs.append(
                    {
                        "time": col[0].replace('"', '').strip()[11:],
                        "index": col[1].replace('\\n"', '').replace(';', '').strip()
                    })
            json_index['CDSET']=indexs
    return json_index

def parse_latest_share_price(soup):
    prices = []
    mkt_prices = {}
    count = 1 
    table = soup.find('table',class_='table table-bordered background-white shares-table fixedHeader')
    keys = ["sl", "symbol", "ltp", "high", "low", "closep", "ycp", "change_val", "trade_count", "value_mn", "volume"]
    for tr in table.find_all("tr"):
        rows = []
        for td in tr.find_all("td"):
            rows.append(td.get_text(strip=True).replace(',','').replace('--','0'))
        if count > 1:
            prices.append(rows)
        count = count + 1
    json_data = [dict(zip(keys, row)) for row in prices]
    mkt_prices["DSE"]=json_data
    return mkt_prices

    # Pretty print
    # print(json.dumps(json_data, indent=4))

def parse_latest_share_price_debt(soup):
    prices = []
    count = 1
    table = soup.find('table',class_='table table-bordered background-white shares-table fixedHeader')
    keys = ["sl", "symbol", "ltp", "high", "low", "closep", "ycp", "change_val", "trade_count", "value_mn", "volume"]
    for tr in table.find_all("tr"):
        rows = []
        for td in tr.find_all("td"):
            rows.append(td.get_text(strip=True).replace(',','').replace('--','0'))
        if count > 1:
            prices.append(rows)
        count = count + 1
    json_data = [dict(zip(keys, row)) for row in prices]
    return json_data
    
def parse_sector_wise_inst(sector_id,soup):
    sector = soup.find("h2", class_="BodyHead topBodyHead").get_text(strip=True).split("\n")[1].strip()
    symbols = [a.get_text(strip=True) for a in soup.find_all("a", class_="ab1") if 'displayCompany' in a['href'] ]
    json_data = {
                'sector_id': sector_id,
                'sector': sector,
                'symbols': symbols
                }
    # print (inst)
    return json_data

def parse_ipo_offer(soup):
   data = []
   table = soup.find("table",class_="table table-bordered table-striped") 
   trs = table.find_all("tr")[1:]
#    print (trs)
   for tr in trs:
    tds = tr.find_all("td")
    if len(tds) >= 3:
        company_name = tds[1].get_text(strip=True)
        link_tag = tds[2].find("a")
        href = link_tag["href"] if link_tag else None
        data.append({"company": company_name, "href": href})
   return data


def parse_dse_news(soup):
    data = []
    table = soup.find("table",class_="table-news") 
    # print (table)
    data = {}
    rows = []
    array = []
    # Extract <th> and <td> pairs
    for row in table.find_all("tr"):
        th = row.find("th")
        td = row.find("td")

        if th and td:
            key = th.get_text(strip=True)
            value = td.get_text(strip=True)
            data[key] = value
        # when a 'Post Date' is found → indicates one full news block
        if "Post Date:" in data:
            rows.append(data.copy()) # store a copy of current record
            data.clear() # reset for next record
        # --- Step 3: Print or save ---
    for r in rows:
        array.append(r)
    return (array)

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
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()
    data['index'] = 'CSE50' 
    all_data.append(data)
    # CSE30
    data = {"selected_index": "CSE30", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()
    data['index'] = 'CSE30' 
    all_data.append(data)
    # CSCX
    data = {"selected_index": "CSCX", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()
    data['index'] = 'CSCX' 
    all_data.append(data)
    # CASPI
    data = {"selected_index": "CASPI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()
    data['index'] = 'CASPI' 
    all_data.append(data)
    # CSI
    data = {"selected_index": "CSI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
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
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSE50'] = idx_data

    # CSE30
    data = {"selected_index": "CSE30", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSE30'] = idx_data

    # CSCX
    data = {"selected_index": "CSCX", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CSCX'] = idx_data

    # CASPI
    data = {"selected_index": "CASPI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
    data =  resp.json()

    idx_data = [{'time':item['idx_time'],'index':item['idx_capital_value']} for item in data]
    idx_title['CASPI'] = idx_data

    # CSI
    data = {"selected_index": "CSI", "csrf_cse_token": csrf_token}
    resp = session.post(post_url, headers=headers, data=data)
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
        title = div.find("strong").get_text(strip=True)
        content = div.find_all("p")[1].get_text(strip=False)

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
            "percent": percent.replace('%',''),
            "arrow": arrow,
        })
    return stocks