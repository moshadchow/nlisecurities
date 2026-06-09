import pymysql
from models.db import get_connection
from decimal import Decimal
import re

def _decimals_to_float(row):
    if row is None:
        return None
    return {k: (float(v) if isinstance(v, Decimal) else v) for k, v in row.items()}

def save_debt_to_db(json_data):
    conn = None
    cursor = None
    try:
        # Connect to MySQL
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE api_debt_prices")
        conn.commit()
        print("🧹 Existing records deleted.")
        # Prepare insert query
        query = """
        INSERT INTO api_debt_prices (
            sl, inst, ltp, high, low, closep, ycp, change_val, trade_count, value_mn, volume
        ) VALUES (%(sl)s, %(inst)s, %(ltp)s, %(high)s, %(low)s, %(closep)s, %(ycp)s,
                  %(change_val)s, %(trade_count)s, %(value_mn)s, %(volume)s)
        """

        # Insert all rows
        cursor.executemany(query, json_data)
        conn.commit()

        print(f"{cursor.rowcount} records inserted successfully.")

    except Exception as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def save_sector_inst_to_db(json_data):
    conn = None
    cursor = None
    try:
        # Connect to MySQL
        conn = get_connection("nlsdb")
        cursor = conn.cursor()

        # Clear old records
        cursor.execute("TRUNCATE TABLE api_sector_inst")
        conn.commit()
        print("🧹 Existing records deleted.")

        # Insert query
        query = """
        INSERT INTO api_sector_inst (sector_id, sector, symbol)
        VALUES (%s, %s, %s)
        """

        rows = []
        # Iterate over each sector in the list
        for sector_item in json_data:
            sector_id = sector_item["sector_id"]
            sector = sector_item["sector"]
            instruments = sector_item.get("symbols", [])
            for inst in instruments:
                rows.append((sector_id, sector, inst))

        # Insert all rows at once
        cursor.executemany(query, rows)
        conn.commit()

        print(f"{cursor.rowcount} records inserted successfully.")

    except Exception as err:
        print("Error:", err)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_ipo_to_db(json_data):
    conn = None
    cursor = None
    try:
        conn = get_connection("nlsdb")
        cursor = conn.cursor()

        # Clear old records
        cursor.execute("TRUNCATE TABLE api_ipo_offer")
        conn.commit()
        print("🧹 Existing records deleted.")

        # Insert query
        query = """
        INSERT INTO api_ipo_offer (company, href)
        VALUES (%s, %s)
        """
        rows = []

        for data in json_data:
            com =  data["company"]
            href =  data["href"]
            rows.append((com,href))
        
        cursor.executemany(query,rows)
        conn.commit()  
        print(f"{cursor.rowcount} records inserted successfully.")

    except Exception as err:
        print("Error:", err)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_news_to_db(market_name,json_data):
    conn = None
    cursor = None
    try:
        conn = get_connection("nlsdb")
        cursor = conn.cursor()

        # Clear old records
        cursor.execute("DELETE from api_marketnews WHERE market = %s", (market_name,))
        conn.commit()
        print(f"Deleted {cursor.rowcount} news for market: {market_name}")
        # Insert query
        query = """
        INSERT INTO api_marketnews (market,trading_code,title,news,publish_date)
        VALUES (%s,%s,%s,%s,%s)
        """
        rows = []

        for data in json_data:
            clean_data = {k.strip(":").strip(): v for k, v in data.items()}
            trading_code = clean_data.get("Trading Code", "")
            title = clean_data.get("News Title", "")
            news = clean_data.get("News", "")
            publish_date = clean_data.get("Post Date", "")
            rows.append((market_name,trading_code,title,news,publish_date))
        
        cursor.executemany(query,rows)
        conn.commit()  
        print(f"{cursor.rowcount} {market_name} news inserted successfully.")

    except Exception as err:
        print("Error:", err)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_prices_to_db(json_data):
    conn = None
    cursor = None
    try:
        conn = get_connection("nlsdb")
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO api_share_prices (
            market, sl, symbol, ltp, high, low, closep, ycp, change_val, trade_count, value_mn, volume
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for market_name, items in json_data.items():
            # Delete old rows for this market once
            cursor.execute("DELETE FROM api_share_prices WHERE market = %s", (market_name,))
            conn.commit()
            print(f"Deleted {cursor.rowcount} rows for market: {market_name}")

            rows_to_insert = [
                (
                    market_name,
                    item.get("sl"),
                    item.get("symbol"),
                    item.get("ltp"),
                    item.get("high"),
                    item.get("low"),
                    item.get("closep") if market_name == "DSE" else item.get("open"),
                    item.get("ycp"),
                    item.get("change_val"),
                    item.get("trade_count"),
                    item.get("value_mn"),
                    item.get("volume"),
                )
                for item in items
            ]

            if rows_to_insert:
                cursor.executemany(insert_query, rows_to_insert)
                print(f"{len(rows_to_insert)} records inserted for market: {market_name}")

        conn.commit()
        print("All records inserted successfully.")

    except Exception as err:
        print("Error:", err)
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_minute_idx_to_db(market,json_data):
    conn = None
    cursor = None
    try:
        # Connect to MySQL
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        # Delete only existing rows for that specific market
        delete_query = "DELETE FROM api_minute_data WHERE market = %s"
        cursor.execute(delete_query, (market,))
        conn.commit()
        print(f"Deleted {cursor.rowcount} rows for market: {market}")
        # Prepare insert query
        insert_query = """
            INSERT INTO api_minute_data (market, name, time, index_val)
            VALUES (%s, %s, %s, %s)
        """
        rows_to_insert = []
        # Insert all rows
        for name, items in json_data.items():
            for item in items:
                raw_index = item.get("index", "")
                match = re.match(r'^\d+(\.\d+)?', raw_index.strip())
                clean_index = match.group(0) if match else None
                rows_to_insert.append((
                    market,
                    name,
                    item.get("time"),
                    clean_index
                ))
        cursor.executemany(insert_query,rows_to_insert)
        conn.commit()

        print(f"{cursor.rowcount} records inserted successfully.")

    except Exception as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

def save_market_idx_to_db(market,json_data):
    try:
         # Connect to MySQL
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        # Delete only existing rows for that specific market
        delete_query = "DELETE FROM api_market_index WHERE market = %s"
        cursor.execute(delete_query, (market,))
        conn.commit()
        print(f"Deleted {cursor.rowcount} rows for market: {market}")
        # Prepare insert query
        insert_query = """
            INSERT INTO api_market_index (market, index_name, index_value, index_change, percentage, arrow)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        rows_to_insert = []

        for item in json_data:
            # Insert only dictionaries that contain an 'index' key
            if "index" in item:
                rows_to_insert.append((
                    market,
                    item.get("index"),
                    item.get("value"),
                    item.get("change"),
                    item.get("percent") if market=='DSE' else item.get("percentage_change"),
                    item.get("arrow")
                ))

        if rows_to_insert:
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            print(f"{len(rows_to_insert)} market index rows inserted.")

        # Extract summary dicts by key presence rather than position
        totals = next((d for d in json_data if "total_trade" in d), {})
        issues = next((d for d in json_data if "issues_advanced" in d), {})

        trade = totals.get("total_trade")
        volume = totals.get("total_volume")
        value = totals.get("total_value")

        advance = issues.get("issues_advanced")
        decline = issues.get("issues_declined")
        unchange = issues.get("issues_unchanged")

        # Delete only existing rows for that specific market
        delete_query = "DELETE FROM api_market_info WHERE market = %s"
        cursor.execute(delete_query, (market,))
        conn.commit()
        print(f"Deleted {cursor.rowcount} rows for market: {market}")

        insert_query = """
            INSERT INTO api_market_info 
            (market, trade, volume, value, advance, decline, unchange)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        row = (market, trade, volume, value, advance, decline, unchange)
        cursor.execute(insert_query, row)
        conn.commit()

        print("market info inserted")


    except Exception as err:
        print("Error:", err)
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_ticker_to_db(market,json_data):
    try:
         # Connect to MySQL
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        # Delete only existing rows for that specific market
        delete_query = "DELETE FROM api_ticker_price WHERE market = %s"
        cursor.execute(delete_query, (market,))
        conn.commit()
        print(f"Deleted {cursor.rowcount} rows for market: {market}")
        # Prepare insert query
        insert_query = """
            INSERT INTO api_ticker_price (market, inst, price, change_val, percent, arrow)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        rows_to_insert = []

        for item in json_data:
            rows_to_insert.append((
                market,
                item.get("inst"),
                item.get("price"),
                item.get("change"),
                item.get("percent"),
                item.get("arrow")
            ))
            
        if rows_to_insert:
            cursor.executemany(insert_query, rows_to_insert)
            conn.commit()
            print(f"{len(rows_to_insert)} market ticker rows inserted.")

    except Exception as err:
        print("Error:", err)
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_ticker_price_from_db(market):
    try:
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        select_query = """
            SELECT market, inst, price, change_val, percent, arrow
            FROM api_ticker_price
            WHERE market = %s
        """
        cursor.execute(select_query, (market,))
        return [_decimals_to_float(row) for row in cursor.fetchall()]
    except Exception as err:
        print("Error:", err)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_market_info_from_db(market):
    try:
        conn = get_connection("nlsdb")
        cursor = conn.cursor()
        select_query = """
            SELECT market, trade, volume, value, advance, decline, unchange
            FROM api_market_info
            WHERE market = %s
        """
        cursor.execute(select_query, (market,))
        return _decimals_to_float(cursor.fetchone())
    except Exception as err:
        print("Error:", err)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()