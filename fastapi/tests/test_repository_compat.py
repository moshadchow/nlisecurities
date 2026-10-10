import re

from conftest import FASTAPI_ROOT, load_html, load_json
from utils import parser as P


def _repo_src():
    import os
    with open(os.path.join(FASTAPI_ROOT, "models", "repository.py"), encoding="utf-8") as fh:
        return fh.read()


def _ddl_cols():
    import os
    with open(os.path.join(FASTAPI_ROOT, "models", "db.py"), encoding="utf-8") as fh:
        src = fh.read()
    tables = dict(re.findall(r'tables\["(\w+)"\]\s*=\s*"""(.*?)"""', src, re.S))
    cols = {}
    for name, body in tables.items():
        found = re.findall(r"^\s*([A-Za-z_]\w*)\s+"
                           r"(INT|VARCHAR|DECIMAL|NUMERIC|TIMESTAMP)\b",
                           body, re.M | re.I)
        cols[name.lower()] = {c[0].lower() for c in found}
    return cols


def test_repository_inserts_match_ddl_columns():
    repo = _repo_src()
    ddl = _ddl_cols()
    inserts = re.findall(r"INSERT INTO\s+(\w+)\s*\(([^)]+)\)", repo, re.I)
    assert len(inserts) >= 9, "expected all repository inserts to be checked"
    for table, column_list in inserts:
        columns = {c.strip().lower() for c in column_list.split(",") if c.strip()}
        assert table.lower() in ddl, "insert into unknown table %s" % table
        missing = columns - ddl[table.lower()]
        assert not missing, "INSERT into %s uses columns absent from DDL: %s" % (
            table, sorted(missing))


def test_debt_insert_uses_symbol_not_inst():
    # regression: api_debt_prices defines `symbol`; the old INSERT said `inst`
    # and silently failed at runtime.
    query = re.search(r"INSERT INTO\s+api_debt_prices\s*\(([^)]+)\)",
                      _repo_src(), re.I | re.S).group(1)
    columns = {c.strip().lower() for c in query.split(",")}
    assert "symbol" in columns
    assert "inst" not in columns


def test_named_placeholders_match_parsed_keys():
    repo = _repo_src()
    block = re.search(r"INSERT INTO\s+api_debt_prices\b(.*?)\"\"\"",
                      repo, re.I | re.S).group(1)
    placeholders = set(re.findall(r"%\((\w+)\)s", block))
    row = P.parse_latest_share_price_debt(load_json("live_prices.json"))[0]
    assert placeholders == set(row), (placeholders, set(row))


def test_news_keys_line_up_with_repository():
    row = P.parse_dse_news(load_json("live_news.json"))[0]
    stripped = {k.strip(":").strip() for k in row}
    assert stripped == {"Trading Code", "News Title", "News", "Post Date"}


def test_ticker_keys_line_up_with_repository():
    row = P.parse_ticker_data(load_html("home_ticker.html"))[0]
    assert set(row) == {"inst", "price", "change", "percent", "arrow"}


def test_minute_items_are_save_compatible():
    series = {
        "DSEX": load_json("index_intraday.json"),
        "DS30": load_json("index_intraday_ds30.json"),
        "DSES": load_json("index_intraday_dses.json"),
    }
    for name, points in P.parse_minute_index(series).items():
        assert len(name) <= 10  # api_minute_data.name VARCHAR(10)
        for point in points:
            assert len(str(point["time"])) <= 8  # VARCHAR(8)
            # save_minute_idx_to_db regex-strips a string index
            assert isinstance(point["index"], str)


def test_market_index_rows_fit_columns():
    data = P.parse_index_data(load_json("live_market.json"))
    for row in data:
        if "index" not in row:
            continue
        assert len(row["index"]) <= 50
        assert row["arrow"] in ("upArrow", "downArrow", "")
        assert len(row["arrow"]) <= 10
        for key in ("value", "change", "percent"):
            assert isinstance(row[key], float)


def test_share_price_rows_fit_columns():
    rows = P.parse_latest_share_price(load_json("live_prices.json"))["DSE"]
    for row in rows:
        assert len(row["symbol"]) <= 20
        assert isinstance(row["sl"], int)
        assert isinstance(row["trade_count"], int)
        assert isinstance(row["volume"], int)
