import inspect

from services import dse_service as S
from utils import parser as P

# Signatures are a public contract: main.py, endpoints and repository call
# these by name and argument position. They must not drift.

EXPECTED_SERVICE = {
    "get_soup": "(BASE_URL, ca_bundle=None)",
    "get_soup_selenium": "(BASE_URL)",
    "get_index_data": "()",
    "get_ticker_data": "()",
    "get_minute_index_data": "()",
    "get_latest_share_price": "()",
    "get_latest_share_price_debt": "()",
    "fetch_all_sector_wise_inst": "()",
    "get_sector_wise_inst": "(sector_id)",
    "get_ipo_offer": "()",
    "get_dse_news": "()",
    "get_index_data_cse": "()",
    "get_minute_index_data_cse": "()",
    "get_latest_share_price_cse": "()",
    "get_cse_news": "()",
    "get_ticker_data_cse": "()",
}

EXPECTED_PARSER = {
    "parse_index_data": "(payload)",
    "parse_ticker_data": "(soup)",
    "parse_minute_index": "(payload)",
    "parse_latest_share_price": "(payload)",
    "parse_latest_share_price_debt": "(payload)",
    "parse_sector_wise_inst": "(sector_id, payload)",
    "parse_ipo_offer": "(soup)",
    "parse_dse_news": "(payload)",
    "parse_index_summary_cse": "(soup, post_url, csrf_token, session)",
    "parse_minute_index_cse": "(post_url, csrf_token, session)",
    "parse_latest_share_price_cse": "(soup)",
    "parse_cse_news": "(soup)",
    "parse_ticker_data_cse": "(soup)",
}


def test_service_signatures():
    for name, expected in EXPECTED_SERVICE.items():
        assert hasattr(S, name), "missing service function: %s" % name
        actual = str(inspect.signature(getattr(S, name)))
        assert actual == expected, "%s signature drifted: %s != %s" % (name, actual, expected)


def test_parser_signatures():
    for name, expected in EXPECTED_PARSER.items():
        assert hasattr(P, name), "missing parser function: %s" % name
        actual = str(inspect.signature(getattr(P, name)))
        assert actual == expected, "%s signature drifted: %s != %s" % (name, actual, expected)


def test_get_dse_news_no_selenium():
    source = inspect.getsource(S.get_dse_news)
    assert "selenium" not in source.lower()
