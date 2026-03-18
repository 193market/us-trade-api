# US Trade Balance API

Real-time US trade balance, exports, and imports data. Powered by FRED (Federal Reserve Economic Data).

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All trade indicators snapshot |
| `GET /trade-balance` | Trade balance in goods and services (BOPGSTB) |
| `GET /exports` | Exports of goods and services (EXPGS) |
| `GET /imports` | Imports of goods and services (IMPGS) |
| `GET /goods-trade` | Trade balance in goods only (BOPGTB) |
| `GET /services-trade` | Trade balance in services only (BOPSTB) |

## Data Source

FRED - Federal Reserve Bank of St. Louis
https://fred.stlouisfed.org/

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
