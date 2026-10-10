import copy
import re

from conftest import load_html, load_json
from utils import parser as P

CSRF = "test-csrf-token"
POST_URL = "https://www.cse.com.bd/home/load__index_summary/"
GRAPH_URL = "https://www.cse.com.bd/home/graph_load/"
INDEX_NAMES = ["CSE50", "CSE30", "CSCX", "CASPI", "CSI"]


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        # a fresh object per call, like a real HTTP response
        return copy.deepcopy(self._payload)


class FakeSession:
    def __init__(self, payload):
        self._payload = payload
        self.calls = []

    def post(self, url, headers=None, data=None, timeout=None):
        self.calls.append({"url": url, "data": dict(data or {}), "timeout": timeout})
        return FakeResponse(self._payload)


def test_index_summary_cse():
    soup = load_html("cse_home.html")
    assert soup.find("input", {"name": "csrf_cse_token"}) is not None

    session = FakeSession(load_json("cse_index_summary.json"))
    data = P.parse_index_summary_cse(soup, POST_URL, CSRF, session)

    assert len(data) == 7
    trade, issues = data[0], data[1]
    assert set(trade) == {"total_value", "total_trade", "total_volume"}
    _as_number(trade["total_value"])
    _as_number(trade["total_trade"])
    _as_number(trade["total_volume"])
    assert set(issues) == {"issues_advanced", "issues_declined", "issues_unchanged"}

    indices = data[2:]
    assert [d["index"] for d in indices] == INDEX_NAMES
    for row in indices:
        assert {"value", "change", "percentage_change"} <= set(row)
        for key in ("value", "change", "percentage_change"):
            _as_number(row[key])

    assert len(session.calls) == 5
    for call, name in zip(session.calls, INDEX_NAMES):
        assert call["url"] == POST_URL
        assert call["data"]["selected_index"] == name
        assert call["data"]["csrf_cse_token"] == CSRF
        assert call["timeout"]


def test_minute_index_cse():
    session = FakeSession(load_json("cse_graph_load.json"))
    data = P.parse_minute_index_cse(GRAPH_URL, CSRF, session)
    assert set(data) == set(INDEX_NAMES)
    for name, points in data.items():
        assert len(points) == 20
        assert set(points[0]) == {"time", "index"}
        for point in points:
            assert re.fullmatch(r"\d{2}:\d{2}:\d{2}", point["time"])
            assert isinstance(point["index"], str)
            match = re.match(r"^\d+(\.\d+)?", point["index"].strip())
            assert match and float(match.group(0)) > 0
    assert len(session.calls) == 5
    assert all(call["data"]["csrf_cse_token"] == CSRF for call in session.calls)


def test_latest_share_price_cse():
    data = P.parse_latest_share_price_cse(load_html("cse_current_price.html"))
    assert set(data) == {"CSE"}
    rows = data["CSE"]
    assert len(rows) == 11
    keys = ["sl", "symbol", "ltp", "open", "high", "low", "ycp",
            "change_val", "trade_count", "value_mn", "volume"]
    assert [r["sl"] for r in rows] == [str(i) for i in range(1, len(rows) + 1)]
    for row in rows:
        assert list(row) == keys
        assert row["symbol"] and len(row["symbol"]) <= 20
        expected_change = round(float(row["ltp"]) - float(row["ycp"]), 2)
        assert float(row["change_val"]) == expected_change
        for key in ("ltp", "open", "high", "low", "ycp"):
            assert float(row[key]) >= 0


def test_cse_news_skips_helper_divs():
    # fixture starts with the strong-less "Show all news" helper div, which
    # used to crash the parser with AttributeError.
    data = P.parse_cse_news(load_html("cse_news.html"))
    assert len(data) == 3
    for row in data:
        assert set(row) == {"Trading Code:", "News Title:", "News:", "Post Date:"}
        assert row["Post Date:"]
        assert row["News:"]
        assert len(row["Trading Code:"]) <= 50


def test_ticker_data_cse():
    stocks = P.parse_ticker_data_cse(load_html("cse_ticker2.html"))
    assert len(stocks) == 6
    for row in stocks:
        assert row["inst"] and len(row["inst"]) <= 20
        assert re.fullmatch(r"\d+(\.\d{1,2})?", row["price"])
        assert row["arrow"] in ("tkup", "tkdown", "tkupdown")
        assert row["percent"] is None or "%" not in row["percent"]


def _as_number(value):
    assert float(str(value).replace(",", "")) == float(str(value).replace(",", ""))
