from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from services.dse_service import (
    get_index_data,
    get_ticker_data,
    get_minute_index_data,
    get_latest_share_price,
    get_latest_share_price_debt,
    fetch_all_sector_wise_inst,
    get_ipo_offer,
    get_dse_news,
    get_index_data_cse,
    get_minute_index_data_cse,
    get_latest_share_price_cse,
    get_cse_news,
    get_ticker_data_cse
)
from models.db import create_database_and_table
from models.repository import (save_prices_to_db,
                 save_debt_to_db,
                 save_sector_inst_to_db,
                 save_ipo_to_db,
                 save_news_to_db,
                 save_minute_idx_to_db,
                 save_market_idx_to_db,
                 save_ticker_to_db,
                 get_ticker_price_from_db,
                 get_market_info_from_db
                 )

import asyncio

async def periodic_runner():
    while True:
        try:
            print("Running periodic tasks...")

            # DSE tasks
            dse_index_data = get_index_data()
            if dse_index_data:
                save_market_idx_to_db("DSE", dse_index_data)

            dse_ticker = get_ticker_data()
            if dse_ticker:
                save_ticker_to_db("DSE", dse_ticker)

            dse_minutes_index = get_minute_index_data()
            if dse_minutes_index:
                save_minute_idx_to_db("DSE",dse_minutes_index)

            dse_share_price = get_latest_share_price()
            if dse_share_price:
                save_prices_to_db(dse_share_price)
            
            dse_ipo_offer = get_ipo_offer()
            if dse_ipo_offer:
                save_ipo_to_db(dse_ipo_offer)

            dse_news = get_dse_news()
            if dse_news:
                save_news_to_db("DSE",dse_news)

            # CSE tasks
            cse_index_data = get_index_data_cse()
            if cse_index_data:
                save_market_idx_to_db("CSE", cse_index_data)

            cse_ticker = get_ticker_data_cse()
            if cse_ticker:
                save_ticker_to_db("CSE", cse_ticker)

            cse_minutes_index = get_minute_index_data_cse()
            if cse_minutes_index:
                save_minute_idx_to_db("CSE",cse_minutes_index)

            cse_share_price = get_latest_share_price_cse()
            if cse_share_price:
                save_prices_to_db(cse_share_price)

            cse_news = get_cse_news()
            if cse_news:
                save_news_to_db("CSE",cse_news)

            print("All periodic jobs done.")

        except Exception as e:
            print("Periodic Runner Error:", e)

        await asyncio.sleep(30)  # wait 30 seconds



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database_and_table()

    # Start periodic job in background
    task = asyncio.create_task(periodic_runner())

    yield

    # Cancel periodic task on shutdown
    task.cancel()
    print("Shutting down...")


app = FastAPI(title="DSE/CSE Market Data API",lifespan=lifespan)

origins = [
    "http://localhost:5173",  # your Vite/React app
    "http://127.0.0.1:5173",  # add both to be safe
    "https://nlisecurities.com",
    "https://www.nlisecurities.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "DSE Market Data API"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/dse_index")
def dse_index():
    try:
        data = get_index_data()
        if data:
            save_market_idx_to_db("DSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )


@app.get("/dse_ticker")
def ticker():
    try:
        data = get_ticker_data()
        if data:
            save_ticker_to_db("DSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

@app.get("/minutes_index")
def minutes_index():
    try:
        data = get_minute_index_data()
        if data:
            save_minute_idx_to_db("DSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    
@app.get("/latest_share_price")
def latest_share_price():
    try:
        data = get_latest_share_price()
        if data:
            save_prices_to_db(data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

@app.get("/latest_share_price_debt")
def latest_share_price():
    try:
        data = get_latest_share_price_debt()
        if data:
            save_debt_to_db(data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

@app.get("/sector_wise_inst")
def sector_wise_inst():
    try:
        sectors = fetch_all_sector_wise_inst()

        if sectors:
            save_sector_inst_to_db(sectors)
            print(f"Inserted {len(sectors)} records into database.")

        return JSONResponse(content=sectors)

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
    
@app.get("/ipo_offer")
def ipo_offer():
    try:
        data = get_ipo_offer()
        if data:
            save_ipo_to_db(data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    
@app.get("/dse_news")
def dse_news():
    try:
        data = get_dse_news()
        if data:
            save_news_to_db("DSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    
#========================CSE========================================#

@app.get("/cse_index")
def cse_index():
    try:
        data = get_index_data_cse()
        if data:
            save_market_idx_to_db("CSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
            return JSONResponse(
                content={"error": str(e)}, 
                status_code=500
            )
    
@app.get("/minutes_index_cse")
def minutes_index_cse():
    try:
        data = get_minute_index_data_cse()
        if data:
            save_minute_idx_to_db("CSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    
@app.get("/latest_share_price_cse")
def latest_share_price_cse():
    try:
        data = get_latest_share_price_cse()
        if data:
            save_prices_to_db(data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )
    
@app.get("/cse_news")
def cse_news():
    try:
        data = get_cse_news()
        if data:
            save_news_to_db("CSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

@app.get("/cse_ticker")
def ticker():
    try:
        data = get_ticker_data_cse()
        if data:
            save_ticker_to_db("CSE",data)
            print(f"Inserted {len(data)} records into database.")
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

@app.get("/ticker_price/{market}")
def ticker_price(market: str):
    try:
        market = market.upper()
        if market not in ("DSE", "CSE"):
            return JSONResponse(content={"error": "Invalid market"}, status_code=400)
        data = get_ticker_price_from_db(market)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/market_info/{market}")
def market_info(market: str):
    try:
        market = market.upper()
        if market not in ("DSE", "CSE"):
            return JSONResponse(content={"error": "Invalid market"}, status_code=400)
        data = get_market_info_from_db(market)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
