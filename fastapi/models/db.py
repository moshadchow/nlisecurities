import pymysql

def get_connection(database=None):
    """Return a PyMySQL connection."""
    conn_params = {
    	"host": "127.0.0.1",
    	"user": "root",
    	"password": "root",
    	"database": "nlsdb",
    	"port": 3306,
    	"cursorclass": pymysql.cursors.DictCursor
    }
    if database:
        conn_params["database"] = database

    return pymysql.connect(**conn_params)

def create_database_and_table():
# Step 1: Connect to MySQL server (no specific DB)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS nlsdb")
    print("✅ Database 'nlsdb' checked/created successfully.")
    cur.close()
    conn.close()

    # Step 2: Connect again, now to the created DB
    conn = get_connection("nlsdb")
    cur = conn.cursor()

    # Step 3: Create table(s)
    tables={}
    tables["api_share_prices"] = """
    CREATE TABLE IF NOT EXISTS api_share_prices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        sl INT,
        symbol VARCHAR(20),
        ltp DECIMAL(10,2),
        high DECIMAL(10,2),
        low DECIMAL(10,2),
        closep DECIMAL(10,2),
        ycp DECIMAL(10,2),
        change_val DECIMAL(10,2),
        trade_count INT,
        value_mn DECIMAL(10,2),
        volume INT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    tables["api_debt_prices"] = """
    CREATE TABLE IF NOT EXISTS api_debt_prices (
        id INT AUTO_INCREMENT PRIMARY KEY,
        sl INT,
        symbol VARCHAR(20),
        ltp DECIMAL(10,2),
        high DECIMAL(10,2),
        low DECIMAL(10,2),
        closep DECIMAL(10,2),
        ycp DECIMAL(10,2),
        change_val DECIMAL(10,2),
        trade_count INT,
        value_mn DECIMAL(10,2),
        volume INT,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    tables["api_sector_inst"] = """
    CREATE TABLE IF NOT EXISTS api_sector_inst (
        id INT AUTO_INCREMENT PRIMARY KEY,    
        sector_id INT,
        sector VARCHAR(30),
        symbol VARCHAR(30)
    )
    """
    tables["api_ipo_offer"] = """
    CREATE TABLE IF NOT EXISTS api_ipo_offer(
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(50),
        href  VARCHAR(100)
    )
    """
    tables["api_MarketNews"] = """
    CREATE TABLE IF NOT EXISTS api_MarketNews(
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        trading_code VARCHAR(50),
        title VARCHAR(100),
        news VARCHAR(1000),
        publish_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    tables["api_minute_data"] = """
    CREATE TABLE IF NOT EXISTS api_minute_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        name VARCHAR(10),
        time VARCHAR(8),
        index_val DECIMAL(12,5)
    )
    """

    tables["api_market_index"] = """
        CREATE TABLE IF NOT EXISTS api_market_index (
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        index_name VARCHAR(50),
        index_value DECIMAL(12,5),
        index_change DECIMAL(9,5),
        percentage DECIMAL(9,5),
        arrow VARCHAR(10)
    )
    """

    tables["api_market_info"] = """
        CREATE TABLE IF NOT EXISTS api_market_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        trade NUMERIC(9),
        volume NUMERIC(15),
        value DECIMAL(9,5),
        advance int,
        decline int,
        unchange int
    )
    """
    tables["api_ticker_price"] = """
        CREATE TABLE IF NOT EXISTS api_ticker_price (
        id INT AUTO_INCREMENT PRIMARY KEY,
        market VARCHAR(3),
        inst VARCHAR(20),
        price DECIMAL(9,2),
        change_val DECIMAL(7,2),
        percent DECIMAL(7,2),
        arrow VARCHAR(10)
    )
    """

    for name,ddl in tables.items():
        try:
            cur.execute(ddl)
            print(f"✅ Table '{name}' checked/created successfully.")
        except Exception as err:
            print(f"❌ Error creating table {name}: {err}")
    conn.commit()
    cur.close()
    conn.close()
