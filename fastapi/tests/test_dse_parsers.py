import math
import re
from datetime import datetime

from conftest import load_html, load_json
from utils import parser as P

SECTOR_EXPECTED = {
    11: "Bank",
    12: "Mutual Funds",
    13: "Engineering",
    14: "Food & Allied",
    15: "Fuel & Power",
    16: "Jute",
    17: "Textile",
    18: "Pharmaceuticals & Chemicals",
    19: "Paper & Printing",
    20: "Services & Real Estate",
    21: "Cement",
    22: "IT Sector",
    23: "Tannery Industries",
    24: "Ceramics Sector",
    25: "Insurance",
    26: "Corporate Bond",
    27: "Telecommunication",
    28: "Financial Institutions",
    88: "G-SEC (T.Bond)",
}


def _price_rows():
    payload = load_json("live_prices.json")
    cols = payload["cols"]
    return payload, cols, {c: i for i, c in enumerate(cols)}


def _assert_finite(value):
    assert isinstance(value, (int, float)) and not isinstance(value, bool)
    assert not math.isnan(value) and not math.isinf(value)


# ---------------------------- market index ----------------------------

def test_index_data_structure():
    data = P.parse_index_data(load_json("live_market.json"))
    assert len(data) == 6
    assert "last_update" in data[0] and isinstance(data[0]["last_update"], str)

    indices = [d for d in data if "index" in d]
    assert [d["index"] for d in indices] == ["DSEX", "DS30", "DSES"]

    totals = next(d for d in data if "total_trade" in d)
    assert isinstance(totals["total_trade"], int)
    assert isinstance(totals["total_volume"], int)
    _assert_finite(totals["total_value"])

    breadth = next(d for d in data if "issues_advanced" in d)
    assert all(isinstance(breadth[k], int) for k in
               ("issues_advanced", "issues_declined", "issues_unchanged"))
    assert breadth["issues_advanced"] > 0


def test_index_data_arrows_match_change_sign():
    data = P.parse_index_data(load_json("live_market.json"))
    for row in data:
        if "index" not in row:
            continue
        _assert_finite(row["value"])
        _assert_finite(row["change"])
        _assert_finite(row["percent"])
        if row["change"] > 0:
            assert row["arrow"] == "upArrow"
        elif row["change"] < 0:
            assert row["arrow"] == "downArrow"
        else:
            assert row["arrow"] == ""


# ---------------------------- ticker ----------------------------

def test_ticker_data_parses_and_dedupes():
    stocks = P.parse_ticker_data(load_html("home_ticker.html"))
    # fixture holds 25 unique anchors plus a repeated one (marquee wrap)
    assert len(stocks) == 25
    assert len({s["inst"] for s in stocks}) == 25
    assert any(s["arrow"] for s in stocks)
    for row in stocks:
        assert row["inst"]
        assert re.fullmatch(r"\d+\.\d{2}", row["price"])
        assert re.fullmatch(r"-?\d+\.\d{2}", row["change"])
        assert re.fullmatch(r"-?\d+\.\d{2}", row["percent"])
        assert row["arrow"] in ("tkup", "tkdown", "")


def test_ticker_data_skips_malformed_anchor():
    from bs4 import BeautifulSoup
    html = (
        '<div class="ticker-track">'
        '<a href="/company/GOODCO"><span>S</span><span>10.00</span><span style="--up">'
        "</span><span>></span><span>0.50</span><span>5.26%</span></a>"
        '<a href="/company/BADCO"><span>S</span></a>'
        "</div>"
    )
    stocks = P.parse_ticker_data(BeautifulSoup(html, "html.parser"))
    assert [s["inst"] for s in stocks] == ["GOODCO"]


# ---------------------------- minute index ----------------------------

def test_minute_index_series():
    series = {
        "DSEX": load_json("index_intraday.json"),
        "DS30": load_json("index_intraday_ds30.json"),
        "DSES": load_json("index_intraday_dses.json"),
    }
    data = P.parse_minute_index(series)
    assert set(data) == {"DSEX", "DS30", "DSES"}  # CDSET is no longer published
    for name, points in data.items():
        assert len(points) == 251
        assert points[0]["time"] == "10:00"
        for point in points:
            assert re.fullmatch(r"\d{1,2}:\d{2}", point["time"])
            # save_minute_idx_to_db runs a regex on a stripped string
            assert isinstance(point["index"], str)
            match = re.match(r"^\d+(\.\d+)?", point["index"].strip())
            assert match and float(match.group(0)) > 0


# ---------------------------- share prices ----------------------------

def test_latest_share_price_public_board_only():
    payload, cols, idx = _price_rows()
    data = P.parse_latest_share_price(payload)
    assert set(data) == {"DSE"}
    rows = data["DSE"]
    expected = [r for r in payload["rows"] if r[idx["board"]] == "PUBLIC"]
    assert len(rows) == len(expected) > 0

    assert [r["sl"] for r in rows] == list(range(1, len(rows) + 1))
    assert {r["symbol"] for r in rows} == {r[idx["code"]] for r in expected}
    # debt board instruments must not leak into the public table
    debt_symbols = {r[idx["code"]] for r in payload["rows"] if r[idx["board"]] == "DEBT"}
    assert not ({r["symbol"] for r in rows} & debt_symbols)


def test_latest_share_price_change_semantics():
    payload, cols, idx = _price_rows()
    for row in P.parse_latest_share_price(payload)["DSE"]:
        assert len(row["symbol"]) <= 20
        for key in ("ltp", "high", "low", "closep", "ycp", "change_val", "value_mn"):
            _assert_finite(row[key])
        assert isinstance(row["trade_count"], int) and row["trade_count"] >= 0
        assert isinstance(row["volume"], int)
        # non-traded rows report 0, exactly like legacy "--"
        if row["ltp"] == 0:
            assert row["change_val"] == 0
        else:
            assert row["change_val"] == round(row["ltp"] - row["ycp"], 2)


def test_latest_share_price_closep_follows_close():
    payload, cols, idx = _price_rows()
    expected_close = {
        r[idx["code"]]: float(r[idx["close"]])
        for r in payload["rows"] if r[idx["board"]] == "PUBLIC"
    }
    for row in P.parse_latest_share_price(payload)["DSE"]:
        assert row["closep"] == round(expected_close[row["symbol"]], 2)


# ---------------------------- debt prices ----------------------------

def test_debt_prices_board():
    payload, cols, idx = _price_rows()
    rows = P.parse_latest_share_price_debt(payload)
    expected = {r[idx["code"]] for r in payload["rows"] if r[idx["board"]] == "DEBT"}
    assert expected, "fixture must contain DEBT rows"
    assert {r["symbol"] for r in rows} == expected
    assert {"ABBLPBOND", "AIBLPBOND", "IBBL2PBOND"} == expected
    assert [r["sl"] for r in rows] == list(range(1, len(rows) + 1))


# ---------------------------- sectors ----------------------------

def test_sector_mapping_legacy_ids_and_names():
    payload = load_json("live_prices.json")
    seen_ids = set()
    for sector_id, expected_name in SECTOR_EXPECTED.items():
        data = P.parse_sector_wise_inst(sector_id, payload)
        assert data["sector_id"] == sector_id
        assert data["sector"] == expected_name
        assert len(expected_name) <= 30  # api_sector_inst.sector VARCHAR(30)
        assert isinstance(data["symbols"], list)
        assert all(isinstance(s, str) and 0 < len(s) <= 30 for s in data["symbols"])
        seen_ids.add(sector_id)
    assert seen_ids == set(range(11, 29)) | {88}


def test_sector_membership_matches_official_labels():
    payload, cols, idx = _price_rows()
    label_by_id = {
        11: "Bank", 12: "MutFund", 13: "Engineering", 14: "FoodAllied",
        15: "FuelPower", 16: "Jute", 17: "Textile", 18: "PharmaChem",
        19: "PaperPrint", 20: "ServRealEst", 21: "Cement", 22: "IT",
        23: "Tannery", 24: "Ceramic", 25: "Insurance", 26: "CorpBond",
        27: "Telecom", 28: "Financial In", 88: "TBond",
    }
    for sector_id, label in label_by_id.items():
        expected = [
            r[idx["code"]] for r in payload["rows"] if r[idx["sector"]] == label
        ]
        assert P.parse_sector_wise_inst(sector_id, payload)["symbols"] == expected


def test_sector_known_members():
    payload = load_json("live_prices.json")
    assert "1JANATAMF" in P.parse_sector_wise_inst(12, payload)["symbols"]
    assert "ACI" in P.parse_sector_wise_inst(18, payload)["symbols"]
    assert "AAMRANET" in P.parse_sector_wise_inst(22, payload)["symbols"]
    assert "TB15Y0428" in P.parse_sector_wise_inst(88, payload)["symbols"]
    assert "ABBLPBOND" in P.parse_sector_wise_inst(26, payload)["symbols"]


def test_sector_unknown_id_raises():
    import pytest
    with pytest.raises(ValueError):
        P.parse_sector_wise_inst(999, load_json("live_prices.json"))


# ---------------------------- IPO ----------------------------

def test_ipo_offer_documents():
    data = P.parse_ipo_offer(load_html("ipo_rsc.html"))
    # 43 documents on the IPO Center; the 101-char APSCL title cannot fit
    # api_ipo_offer.company VARCHAR(50) and is skipped.
    assert len(data) == 42
    assert len({(d["company"], d["href"]) for d in data}) == len(data)
    for row in data:
        assert 0 < len(row["company"]) <= 50
        assert "\u2014" not in row["company"]  # em dash never leaks into company
        assert row["href"].startswith("/")
        assert len(row["href"]) <= 100
    assert {"company": "Techno Drugs Limited",
            "href": "/api/pageDocuments/file/Prospectus-TDL-1.pdf"} in data
    assert not any(d["company"].startswith("APSCL Non-Convertible") for d in data)


# ---------------------------- news ----------------------------

def test_dse_news_records():
    data = P.parse_dse_news(load_json("live_news.json"))
    assert len(data) == 25
    keys = {"Trading Code:", "News Title:", "News:", "Post Date:"}
    for row in data:
        assert set(row) == keys
        assert len(row["Trading Code:"]) <= 50
        assert len(row["News Title:"]) <= 100
        assert len(row["News:"]) <= 1000
        assert row["News Title:"]
        assert row["News:"]
        datetime.strptime(row["Post Date:"], "%Y-%m-%d %H:%M")
