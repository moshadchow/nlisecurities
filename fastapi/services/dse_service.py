import requests
import certifi
import os
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Both dsebd.org and cse.com.bd omit intermediate certs from their TLS handshakes.
# We ship pre-built bundles (certifi roots + the missing intermediate) for each.
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
DSE_CA_BUNDLE = os.path.join(_BASE, "dse_ca_bundle.pem")
CSE_CA_BUNDLE = os.path.join(_BASE, "cse_ca_bundle.pem")

session = requests.Session()
session.verify = CSE_CA_BUNDLE

def get_soup(BASE_URL, ca_bundle=None):
    verify = ca_bundle if ca_bundle else DSE_CA_BUNDLE
    response = requests.get(BASE_URL, verify=verify)
    if response.status_code != 200:
        raise Exception("Failed to fetch DSE website.")
    return BeautifulSoup(response.text, "html.parser")

def get_soup_selenium(BASE_URL):
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

def get_index_data():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_index_data(soup)

def get_ticker_data():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_ticker_data(soup)

def get_minute_index_data():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_minute_index(soup)

def get_latest_share_price():
    BASE_URL = "https://www.dsebd.org/latest_share_price_scroll_by_ltp.php"
    soup = get_soup(BASE_URL)
    return parse_latest_share_price(soup)

def get_latest_share_price_debt():
    BASE_URL = "https://www.dsebd.org/latest_share_price_scroll_treasury_bond.php"
    soup = get_soup(BASE_URL)
    return parse_latest_share_price_debt(soup)

def fetch_all_sector_wise_inst():
    sectors = []
    # your sector IDs
    SECTOR_IDS = list(range(11, 29)) + [88]

    for s in SECTOR_IDS:
        data = get_sector_wise_inst(s)
        sectors.append(data)

    return sectors

def get_sector_wise_inst(sector_id):
    BASE_URL = f"https://www.dsebd.org/companylistbyindustry.php?industryno={sector_id}"
    soup = get_soup(BASE_URL)
    return parse_sector_wise_inst(sector_id,soup)

def get_ipo_offer():
    BASE_URL = "https://www.dsebd.org/ipo-archive-2024.php"
    soup = get_soup(BASE_URL)
    return parse_ipo_offer(soup)

def get_dse_news():
    BASE_URL = "https://www.dsebd.org/display_news.php"
    soup = get_soup_selenium(BASE_URL)
    return parse_dse_news(soup)

#========================CSE========================================#

def get_index_data_cse():

    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url).text
    soup = BeautifulSoup(html, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_cse_token"})["value"]
    post_url = "https://www.cse.com.bd/home/load__index_summary/"
    return parse_index_summary_cse(soup,post_url,csrf_token,session)


def get_minute_index_data_cse():
    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url).text
    soup = BeautifulSoup(html, "html.parser")

    csrf_token = soup.find("input", {"name": "csrf_cse_token"})["value"]
    post_url = "https://www.cse.com.bd/home/graph_load/"
    return parse_minute_index_cse(post_url,csrf_token,session)

def get_latest_share_price_cse():
    BASE_URL = "https://www.cse.com.bd/market/current_price"
    soup = get_soup(BASE_URL, ca_bundle=CSE_CA_BUNDLE)
    return parse_latest_share_price_cse(soup)

def get_cse_news():
    BASE_URL = "https://www.cse.com.bd/media/news"
    html = session.get(BASE_URL).text
    soup = BeautifulSoup(html, "html.parser")
    # soup = get_soup(BASE_URL)
    return parse_cse_news(soup)

def get_ticker_data_cse():
    BASE_URL = "https://www.cse.com.bd/ticker2.php"
    soup = get_soup(BASE_URL, ca_bundle=CSE_CA_BUNDLE)
    return parse_ticker_data_cse(soup)