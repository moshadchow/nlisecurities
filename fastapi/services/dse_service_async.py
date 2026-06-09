import requests
from bs4 import BeautifulSoup
from utils.parser import (
    parse_index_summary,
    parse_ticker_data,
    parse_board_index,
    parse_latest_share_price,
    parse_latest_share_price_debt,
    parse_sector_wise_inst,
    parse_ipo_offer,
    parse_dse_news,
    parse_index_summary_cse,
    parse_board_index_cse,
    parse_latest_share_price_cse,
    parse_cse_news,
    parse_ticker_data_cse,
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import asyncio

session = requests.Session()


def get_soup(BASE_URL: str) -> BeautifulSoup:
    response = requests.get(BASE_URL, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {BASE_URL} (status {response.status_code})")
    return BeautifulSoup(response.text, "html.parser")


def get_soup_selenium(BASE_URL: str) -> BeautifulSoup:
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
        raise Exception("Failed to fetch DSE website content via Selenium.")

    return BeautifulSoup(html, "html.parser")


# ======================== DSE SYNC WORKERS ======================== #

def _get_index_data_sync():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_index_summary(soup)


def _get_ticker_data_sync():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_ticker_data(soup)


def _get_board_index_data_sync():
    BASE_URL = "https://www.dsebd.org/index.php"
    soup = get_soup(BASE_URL)
    return parse_board_index(soup)


def _get_latest_share_price_sync():
    BASE_URL = "https://www.dsebd.org/latest_share_price_scroll_by_ltp.php"
    soup = get_soup(BASE_URL)
    return parse_latest_share_price(soup)


def _get_latest_share_price_debt_sync():
    BASE_URL = "https://www.dsebd.org/latest_share_price_scroll_treasury_bond.php"
    soup = get_soup(BASE_URL)
    return parse_latest_share_price_debt(soup)


def _get_sector_wise_inst_sync(sector_id: int):
    BASE_URL = f"https://www.dsebd.org/companylistbyindustry.php?industryno={sector_id}"
    soup = get_soup(BASE_URL)
    return parse_sector_wise_inst(sector_id, soup)


def _get_ipo_offer_sync():
    BASE_URL = "https://www.dsebd.org/ipo-archive-2024.php"
    soup = get_soup(BASE_URL)
    return parse_ipo_offer(soup)


def _get_dse_news_sync():
    BASE_URL = "https://www.dsebd.org/display_news.php"
    soup = get_soup_selenium(BASE_URL)
    return parse_dse_news(soup)


# ======================== CSE SYNC WORKERS ======================== #

def _get_index_data_cse_sync():
    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf_cse_token"})["value"]
    post_url = "https://www.cse.com.bd/home/load__index_summary/"
    return parse_index_summary_cse(soup, post_url, csrf_token, session)


def _get_board_index_data_cse_sync():
    home_url = "https://www.cse.com.bd/"
    html = session.get(home_url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")

    csrf_token = soup.find("input", {"name": "csrf_cse_token"})["value"]
    post_url = "https://www.cse.com.bd/home/graph_load/"
    return parse_board_index_cse(post_url, csrf_token, session)


def _get_latest_share_price_cse_sync():
    BASE_URL = "https://www.cse.com.bd/market/current_price"
    soup = get_soup(BASE_URL)
    return parse_latest_share_price_cse(soup)


def _get_cse_news_sync():
    BASE_URL = "https://www.cse.com.bd/media/news"
    html = session.get(BASE_URL, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    return parse_cse_news(soup)


def _get_ticker_data_cse_sync():
    BASE_URL = "https://www.cse.com.bd/ticker2.php"
    soup = get_soup(BASE_URL)
    return parse_ticker_data_cse(soup)


# ======================== ASYNC PUBLIC API ======================== #
# These are what FastAPI endpoints should call.

async def get_index_data():
    return await asyncio.to_thread(_get_index_data_sync)


async def get_ticker_data():
    return await asyncio.to_thread(_get_ticker_data_sync)


async def get_board_index_data():
    return await asyncio.to_thread(_get_board_index_data_sync)


async def get_latest_share_price():
    return await asyncio.to_thread(_get_latest_share_price_sync)


async def get_latest_share_price_debt():
    return await asyncio.to_thread(_get_latest_share_price_debt_sync)


async def get_sector_wise_inst(sector_id: int):
    return await asyncio.to_thread(_get_sector_wise_inst_sync, sector_id)


async def get_ipo_offer():
    return await asyncio.to_thread(_get_ipo_offer_sync)


async def get_dse_news():
    # Still uses Selenium internally but now off the main event loop thread
    return await asyncio.to_thread(_get_dse_news_sync)


# ======================== CSE ASYNC API ======================== #

async def get_index_data_cse():
    return await asyncio.to_thread(_get_index_data_cse_sync)


async def get_board_index_data_cse():
    return await asyncio.to_thread(_get_board_index_data_cse_sync)


async def get_latest_share_price_cse():
    return await asyncio.to_thread(_get_latest_share_price_cse_sync)


async def get_cse_news():
    return await asyncio.to_thread(_get_cse_news_sync)


async def get_ticker_data_cse():
    return await asyncio.to_thread(_get_ticker_data_cse_sync)
