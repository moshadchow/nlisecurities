import math

import pytest
from bs4 import BeautifulSoup

from conftest import load_html, load_json
from utils import parser as P


# --------------------------- helpers ---------------------------

def test_as_float_accepts_numbers_and_numeric_strings():
    assert P._as_float(3) == 3.0
    assert P._as_float("1,234.50") == 1234.5
    assert P._as_float("2.94%") == 2.94
    assert P._as_float("\u22123.2") == -3.2  # unicode minus from the site
    assert P._as_float("--") is None


def test_as_float_rejects_unusable_values():
    for bad in (None, True, False, float("nan"), float("inf"), -float("inf"),
                "abc", "", "--", object(), [1]):
        assert P._as_float(bad) is None


def test_as_int_rejects_unusable_values():
    assert P._as_int("172590") == 172590
    assert P._as_int(None) is None
    assert P._as_int(float("nan")) is None


def _assert_no_nonfinite(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            _assert_no_nonfinite(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            _assert_no_nonfinite(value)
    elif isinstance(obj, float):
        assert not math.isnan(obj) and not math.isinf(obj)


# --------------------------- DSE failure modes ---------------------------

def test_index_data_rejects_non_object():
    with pytest.raises(ValueError):
        P.parse_index_data(None)
    with pytest.raises(ValueError):
        P.parse_index_data({})


def test_index_data_rejects_garbage_rows():
    payload = {
        "totals": {"trades": "not-a-number", "volume": None, "turnover": float("nan")},
        "breadth": {"advanced": 1},
        "indices": [
            {"key": "DSEX", "value": float("nan"), "change": 1, "percent": 1},
            {"key": "", "value": 1, "change": 1, "percent": 1},
            {"key": "DS30", "value": 1, "change": 1, "percent": 1},
        ],
    }
    data = P.parse_index_data(payload)
    assert [d.get("index") for d in data if "index" in d] == ["DS30"]
    _assert_no_nonfinite(data)


def test_ticker_data_requires_track():
    with pytest.raises(ValueError):
        P.parse_ticker_data(BeautifulSoup("<html><body></body></html>", "html.parser"))
    with pytest.raises(ValueError):
        P.parse_ticker_data(None)


def test_ticker_data_requires_any_valid_anchor():
    html = '<div class="ticker-track"><a href="/company/X/"><span>x</span></a></div>'
    with pytest.raises(ValueError):
        P.parse_ticker_data(BeautifulSoup(html, "html.parser"))


def test_minute_index_requires_series():
    with pytest.raises(ValueError):
        P.parse_minute_index({})
    with pytest.raises(ValueError):
        P.parse_minute_index({"DSEX": {"points": [{"t": "10:00", "value": None}]}})
    with pytest.raises(ValueError):
        P.parse_minute_index(None)


def test_prices_require_rows_and_columns():
    with pytest.raises(ValueError):
        P.parse_latest_share_price({"cols": [], "rows": []})
    with pytest.raises(ValueError):
        P.parse_latest_share_price({"rows": []})
    with pytest.raises(ValueError):
        P.parse_latest_share_price(None)
    with pytest.raises(ValueError):
        P.parse_latest_share_price_debt({"cols": ["code"], "rows": []})


def test_prices_skip_malformed_rows_without_corrupting_output():
    cols = ["code", "ltp", "high", "low", "close", "ycp", "trades",
            "value", "volume", "board"]
    rows = [
        ["GOOD", 10.0, 10.5, 9.5, 10.2, 9.8, 100, 1.5, 5000, "PUBLIC"],
        ["BAD-NAN", float("nan"), 1, 1, 1, 1, 1, 1, 1, "PUBLIC"],
        ["BAD-EMPTY", None, 1, 1, 1, 1, 1, 1, 1, "PUBLIC"],
        ["BAD-COUNT", 10, 1, 1, 1, 1, None, 1, 1, "PUBLIC"],
        [None, 10, 1, 1, 1, 1, 1, 1, 1, "PUBLIC"],
    ]
    data = P.parse_latest_share_price({"cols": cols, "rows": rows})["DSE"]
    assert [r["symbol"] for r in data] == ["GOOD"]
    _assert_no_nonfinite(data)


def test_dse_news_requires_valid_rows():
    with pytest.raises(ValueError):
        P.parse_dse_news({"rows": []})
    with pytest.raises(ValueError):
        P.parse_dse_news({"rows": [{"summary": "x", "body": None}]})
    with pytest.raises(ValueError):
        P.parse_dse_news(None)


def test_dse_news_rejects_bad_rows_but_keeps_good_ones():
    good = {
        "id": 1, "code": "EXCH", "summary": "Title", "body": "Body text",
        "filedAt": "2026-10-08", "time": "14:31",
    }
    rows = [
        good,
        dict(good, id=2, time="not-a-time"),
        dict(good, id=3, summary=""),
        dict(good, id=4, summary="x" * 101),
        dict(good, id=1),  # duplicate id
    ]
    data = P.parse_dse_news({"rows": rows})
    assert len(data) == 1
    assert data[0]["Post Date:"] == "2026-10-08 14:31"


def test_ipo_offer_requires_payload():
    with pytest.raises(ValueError):
        P.parse_ipo_offer(BeautifulSoup("<html></html>", "html.parser"))
    with pytest.raises(ValueError):
        P.parse_ipo_offer(None)


def test_ipo_offer_rejects_overlength_href():
    # valid-shaped RSC payload with one over-length href
    files = '{"files":{"circulars":[{"documents":[' \
            '{"title":"Some Company Limited \u2014 Prospectus","href":"' + "/" + "a" * 100 + '"},' \
            '{"title":"Other Co Limited \u2014 Prospectus","href":"/ok.pdf"}]}]}}'
    html = '<html><body><script>self.__next_f.push([1,' + \
           _js_string(files) + '])</script></body></html>'
    data = P.parse_ipo_offer(BeautifulSoup(html, "html.parser"))
    assert len(data) == 1
    assert data[0]["company"] == "Other Co Limited"
    assert data[0]["href"] == "/ok.pdf"


def _js_string(text):
    import json
    return json.dumps(text)


# --------------------------- CSE failure modes ---------------------------

def test_cse_news_handles_page_without_items():
    soup = BeautifulSoup('<html><body><div class="news_content">'
                         "<p>x</p><p>y</p></div></body></html>", "html.parser")
    assert P.parse_cse_news(soup) == []


def test_cse_price_parser_requires_table():
    with pytest.raises(AttributeError):
        P.parse_latest_share_price_cse(BeautifulSoup("<html></html>", "html.parser"))
