import requests
import certifi
import os
import time
from bs4 import BeautifulSoup
from utils.parser import (
    parse_index_data,
    parse_ticker_data,
    parse_minute_index,
    parse_latest_share_price,
    parse_latest_share_price_debt,
    parse_sector_wise_inst,
    parse_ipo_offer,
    parse_dse_news,
    parse_index_summary_cse,
    parse_minute_index_cse,
    parse_latest_share_price_cse,
    parse_cse_news,
    parse_ticker_data_cse
)

# Both dsebd.org (legacy) and cse.com.bd omit intermediate certs from their TLS handshakes.
# We ship pre-built bundles (certifi roots + the missing intermediate) for each.
# The bundles are gitignored; if the DSE bundle is absent we fall back to the certifi
# root store, which successfully verifies www.dse.com.bd. CSE still requires its bundle.
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
DSE_CA_BUNDLE = os.path.join(_BASE, "dse_ca_bundle.pem")
CSE_CA_BUNDLE = os.path.join(_BASE, "cse_ca_bundle.pem")

# New official DSE website (replaces legacy www.dsebd.org, which now 410s).
DSE_BASE = "https://www.dse.com.bd"

_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
_REQUEST_TIMEOUT = (10, 30)
_MAX_RETRIES = 2
_RETRY_BACKOFF = (1.0, 3.0)

session = requests.Session()
session.verify = CSE_CA_BUNDLE


def _sleep(seconds):
    time.sleep(seconds)


def _dse_verify(ca_bundle=None):
    bundle = ca_bundle if ca_bundle else DSE_CA_BUNDLE
    if bundle and os.path.exists(bundle):
        return bundle
    if ca_bundle:
        # Caller explicitly requested a bundle that is not on disk.
        return bundle
    return True  # default certifi store


def _http_get(url, verify, headers=None):
    """GET with explicit timeouts and bounded retries for transient failures."""
    last_error = None
    for attempt in range(_MAX_RETRIES + 1):
        try:
            response = requests.get(
                url,
                timeout=_REQUEST_TIMEOUT,
                verify=verify,
                headers=headers,
            )
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_error = exc
            if attempt < _MAX_RETRIES:
                _sleep(_RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)])
            continue

        if response.status_code == 429 or response.status_code >= 500:
            last_error = Exception("HTTP %s" % response.status_code)
            if attempt < _MAX_RETRIES:
                _sleep(_RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)])
            continue

        if response.status_code != 200:
            raise Exception("Failed to fetch %s (status %s)." % (url, response.status_code))
        return response

    raise Exception("Failed to fetch %s after retries: %s" % (url, last_error))


def get_json(url):
    """Fetch and decode a JSON endpoint from the official DSE website."""
    response = _http_get(
        url,
        verify=_dse_verify(),
        headers={"Accept": "application/json", "User-Agent": _USER_AGENT},
    )
    content_type = response.headers.get("Content-Type", "")
    if "json" not in content_type:
        raise Exception("Unexpected content-type from %s: %s" % (url, content_type))
    try:
        return response.json()
    except ValueError as exc:
        raise Exception("Invalid JSON from %s: %s" % (url, exc))


def get_html(url):
    """Fetch an HTML page from the official DSE website."""
    response = _http_get(
        url,
        verify=_dse_verify(),
        headers={"User-Agent": _USER_AGENT},
    )
    content_type = response.headers.get("Content-Type", "")
    if content_type and "html" not in content_type:
        raise Exception("Unexpected content-type from %s: %s" % (url, content_type))
    return BeautifulSoup(response.text, "html.parser")


def get_soup(BASE_URL, ca_bundle=None):
    verify = ca_bundle if ca_bundle else DSE_CA_BUNDLE
    response = requests.get(BASE_URL, verify=verify, timeout=_REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception("Failed to fetch DSE website.")
    return BeautifulSoup(response.text, "html.parser")

def get_soup_selenium(BASE_URL):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(BASE_URL)
        time.sleep(5)  # Wait for page content to fully load
        html = driver.page_source
    finally:
        driver.quit()

    if not html:
        raise Exception("Failed to fetch DSE website content.")

    return BeautifulSoup(html, "html.parser")


# Live prices feed is shared by the share-price, debt-price and sector functions.
# Cache it briefly so fetch_all_sector_wise_inst does not re-download it per sector.
_PRICES_URL = DSE_BASE + "/api/live/prices"
_PRICES_CACHE = {"at": 0.0, "data": None}
_PRICES_CACHE_TTL = 30.0


def _get_live_prices():
    now = time.time()
    cached = _PRICES_CACHE["data"]
    if cached is not None and (now - _PRICES_CACHE["at"]) < _PRICES_CACHE_TTL:
        return cached
    data = get_json(_PRICES_URL)
    if not isinstance(data, dict) or not isinstance(data.get("cols"), list) or not isinstance(data.get("rows"), list):
        raise Exception("Unexpected /api/live/prices payload structure.")
    _PRICES_CACHE["at"] = now
    _PRICES_CACHE["data"] = data
    return data


def get_index_data():
    payload = get_json(DSE_BASE + "/api/live/market")
    return parse_index_data(payload)

def get_ticker_data():
    soup = get_html(DSE_BASE + "/")
    return parse_ticker_data(soup)

def get_minute_index_data():
    series = {}
    for code in ("DSEX", "DS30", "DSES"):
        series[code] = get_json(DSE_BASE + "/api/live/index-intraday?code=%s" % code)
    return parse_minute_index(series)

def get_latest_share_price():
    payload = _get_live_prices()
    return parse_latest_share_price(payload)

def get_latest_share_price_debt():
    payload = _get_live_prices()
    return parse_latest_share_price_debt(payload)

def fetch_all_sector_wise_inst():
    sectors = []
    # your sector IDs
    SECTOR_IDS = list(range(11, 29)) + [88]

    for s in SECTOR_IDS:
        data = get_sector_wise_inst(s)
        sectors.append(data)

    return sectors

def get_sector_wise_inst(sector_id):
    payload = _get_live_prices()
    return parse_sector_wise_inst(sector_id, payload)

def get_ipo_offer():
    soup = get_html(DSE_BASE + "/ipo")
    return parse_ipo_offer(soup)

def get_dse_news():
    payload = get_json(DSE_BASE + "/api/live/news")
    return parse_dse_news(payload)

#========================CSE========================================#

def get_index_data_cse():

    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url, timeout=_REQUEST_TIMEOUT).text
    soup = BeautifulSoup(html, "html.parser")
    csrf_input = soup.find("input", {"name": "csrf_cse_token"})
    if csrf_input is None or not csrf_input.get("value"):
        raise Exception("CSE CSRF token not found on homepage.")
    csrf_token = csrf_input["value"]
    post_url = "https://www.cse.com.bd/home/load__index_summary/"
    return parse_index_summary_cse(soup,post_url,csrf_token,session)


def get_minute_index_data_cse():
    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url, timeout=_REQUEST_TIMEOUT).text
    soup = BeautifulSoup(html, "html.parser")

    csrf_input = soup.find("input", {"name": "csrf_cse_token"})
    if csrf_input is None or not csrf_input.get("value"):
        raise Exception("CSE CSRF token not found on homepage.")
    csrf_token = csrf_input["value"]
    post_url = "https://www.cse.com.bd/home/graph_load/"
    return parse_minute_index_cse(post_url,csrf_token,session)

def get_latest_share_price_cse():
    BASE_URL = "https://www.cse.com.bd/market/current_price"
    soup = get_soup(BASE_URL, ca_bundle=CSE_CA_BUNDLE)
    return parse_latest_share_price_cse(soup)

def get_cse_news():
    BASE_URL = "https://www.cse.com.bd/media/news"
    html = session.get(BASE_URL, timeout=_REQUEST_TIMEOUT).text
    soup = BeautifulSoup(html, "html.parser")
    # soup = get_soup(BASE_URL)
    return parse_cse_news(soup)

def get_ticker_data_cse():
    BASE_URL = "https://www.cse.com.bd/ticker2.php"
    soup = get_soup(BASE_URL, ca_bundle=CSE_CA_BUNDLE)
    return parse_ticker_data_cse(soup)
