from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from datetime import datetime

app = FastAPI(
    title="US Trade Balance API",
    description="Real-time US trade balance, exports, and imports data. Powered by FRED (Federal Reserve Economic Data).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
API_KEY = os.environ.get("FRED_API_KEY", "")


async def fetch_fred(series_id: str, limit: int = 12):
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(BASE_URL, params={
            "series_id": series_id,
            "api_key": API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        })
        data = res.json()
        return data.get("observations", [])


@app.get("/")
def root():
    return {
        "api": "US Trade Balance API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "endpoints": ["/summary", "/trade-balance", "/exports", "/imports", "/goods-trade", "/services-trade"],
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/summary")
async def summary(limit: int = Query(default=10, ge=1, le=60)):
    """All trade indicators snapshot"""
    trade_balance, exports, imports = await asyncio.gather(
        fetch_fred("BOPGSTB", limit),
        fetch_fred("EXPGS", limit),
        fetch_fred("IMPGS", limit),
    )
    return {
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": {
            "trade_balance": trade_balance,
            "exports": exports,
            "imports": imports,
        }
    }


@app.get("/trade-balance")
async def trade_balance(limit: int = Query(default=12, ge=1, le=60)):
    """US trade balance in goods and services"""
    data = await fetch_fred("BOPGSTB", limit)
    return {
        "indicator": "US Trade Balance: Goods and Services",
        "series_id": "BOPGSTB",
        "unit": "Millions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/exports")
async def exports(limit: int = Query(default=12, ge=1, le=60)):
    """US exports of goods and services"""
    data = await fetch_fred("EXPGS", limit)
    return {
        "indicator": "Exports of Goods and Services",
        "series_id": "EXPGS",
        "unit": "Billions of Dollars",
        "frequency": "Quarterly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/imports")
async def imports(limit: int = Query(default=12, ge=1, le=60)):
    """US imports of goods and services"""
    data = await fetch_fred("IMPGS", limit)
    return {
        "indicator": "Imports of Goods and Services",
        "series_id": "IMPGS",
        "unit": "Billions of Dollars",
        "frequency": "Quarterly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/goods-trade")
async def goods_trade(limit: int = Query(default=12, ge=1, le=60)):
    """US trade balance in goods only"""
    data = await fetch_fred("BOPGTB", limit)
    return {
        "indicator": "US Trade Balance: Goods",
        "series_id": "BOPGTB",
        "unit": "Millions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/services-trade")
async def services_trade(limit: int = Query(default=12, ge=1, le=60)):
    """US trade balance in services only"""
    data = await fetch_fred("BOPSTB", limit)
    return {
        "indicator": "US Trade Balance: Services",
        "series_id": "BOPSTB",
        "unit": "Millions of Dollars",
        "frequency": "Monthly",
        "source": "FRED - Bureau of Economic Analysis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
