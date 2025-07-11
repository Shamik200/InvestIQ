import json
from fastapi import APIRouter, BackgroundTasks, HTTPException
import pandas as pd
from pydantic import BaseModel
from live.papertrader import run, fetch_ohlcv, add_indicators  # ✅ your function
import os
from threading import Thread
from multiprocessing import Process
from backend.state import state
from fastapi.responses import JSONResponse
from backend.model_trainer import train_all_models

router = APIRouter()
bot_thread = None

class TradingRequest(BaseModel):
    symbol: str
    timeframe: str

@router.post("/start")
async def start_bot(data: TradingRequest):
    global bot_thread
    if not state.running:
        state.running = True
        bot_thread = Thread(target=run, args=(data.symbol, data.timeframe), daemon=True)
        bot_thread.start()
        return {"status": "started"}
    return {"status": "already running"}

@router.post("/stop")
async def stop_bot():
    state.running = False
    return {"status": "stopping"}

@router.get("/chart")
def get_chart(symbol: str, timeframe: str):
    print(f"Chart request: symbol={symbol}, timeframe={timeframe}")

    # Optional: map numeric timeframes like '1' to '1m'
    if timeframe.isdigit():
        timeframe += "m"

    try:
        df = fetch_ohlcv(symbol, timeframe)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="No OHLCV data found.")

        df = add_indicators(df)

        data = []
        for _, row in df.iterrows():
            try:
                ts = int(pd.to_datetime(row["timestamp"]).timestamp()) if not isinstance(row["timestamp"], int) else int(row["timestamp"] / 1000)
                data.append({
                    "timestamp": ts,
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "entry": bool(row.get("entry", False)),
                    "exit": bool(row.get("exit", False)),
                })
            except Exception as e:
                print(f"Row parse error: {e}")
                continue

        return data

    except Exception as e:
        print(f"Error in /chart endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


trade_logs = []  # Ideally, replace with a DB in future

@router.get("/trades")
def get_trades():
    log_path = 'logs/trades.json'
    
    # Ensure logs/trades.json exists and is valid JSON
    if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w') as f:
            json.dump([], f)

    # Load trade data
    with open(log_path, 'r') as f:
        data = json.load(f)

    return data


# @router.post("/trades")
# def add_trade_log(trade: dict):
#     trade_logs.append(trade)
#     return {"status": "added", "trade": trade}

# @router.get("/marks")
# def get_trade_marks():
#     marks = []
#     for trade in trade_logs:
#         marks.append({
#             "timestamp": trade["timestamp"],  # should be in epoch seconds or ISO
#             "price": trade["price"],
#             "type": trade["type"]
#         })
#     return marks

@router.get("/total_profit")
def get_total_profit():
    total = 0
    try:
        if os.path.exists("logs/trades.json"):
            with open("logs/trades.json", "r") as f:
                trade_logs = json.load(f)
            for trade in trade_logs:
                if "pnl" in trade and trade["pnl"] is not None:
                    total += trade["pnl"]
    except Exception as e:
        print("❌ Error calculating total profit:", e)
        return JSONResponse(content={"error": "Failed to calculate total profit"}, status_code=500)

    return {"total_profit": round(total, 2)}

@router.get("/signals")
def get_signals():
    try:
        with open("logs/signals.json", "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except:
        return JSONResponse(content=[])

from fastapi.responses import JSONResponse

# @router.get("/marks")
# def get_marks():
#     try:
#         with open("logs/marks.json", "r") as f:
#             return JSONResponse(content=json.load(f))
#     except:
#         return JSONResponse(content=[])



class TrainRequest(BaseModel):
    symbol: str
    timeframe: str

@router.post("/train_model")
async def train_model(request: TrainRequest):
    # Remove 'm', 'h', 'd' suffixes
    try:
        train_all_models(request.symbol, request.timeframe)
        return {"message": "Training completed and models saved."}
    except Exception as e:
        return {"error": str(e)}