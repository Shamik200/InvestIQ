import pandas as pd
import ccxt
import ta
import os
import joblib
import time
import numpy as np
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_utils import append_live_data
import requests
import json
from backend.state import state

trades = []

# symbol = "BTC/USDT"
capital = 1000
position = None
entry_price = 0.0
balance = capital
quantity = 0
entry_time = None

# Load binary classifier models
models = [
    joblib.load("models/xgb_clf_tuned.pkl"),
    joblib.load("models/lgbm_clf_tuned.pkl"),
    joblib.load("models/rf_clf_tuned.pkl")
]

FEATURES = [
    'rsi', 'macd', 'macd_signal', 'macd_diff',
    'sma_50', 'ema_21', 'atr', 'body', 'upper_wick', 'lower_wick',
    'return_1', 'return_3', 'rolling_std', 'volume_spike',
    'price_above_ema', 'rsi_oversold', 'macd_cross_up',
    'volatility', 'momentum_3'
]

exchange = ccxt.bybit()

def fetch_ohlcv(symbol: str, timeframe:str):
    df = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(df, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def add_indicators(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    df["macd_diff"] = macd.macd_diff()
    df["sma_50"] = ta.trend.SMAIndicator(df["close"], 50).sma_indicator()
    df["ema_21"] = ta.trend.EMAIndicator(df["close"], 21).ema_indicator()
    df["atr"] = ta.volatility.AverageTrueRange(df["high"], df["low"], df["close"]).average_true_range()
    df["body"] = df["close"] - df["open"]
    df["upper_wick"] = df["high"] - df[["close", "open"]].max(axis=1)
    df["lower_wick"] = df[["close", "open"]].min(axis=1) - df["low"]
    df["return_1"] = df["close"].pct_change()
    df["return_3"] = df["close"].pct_change(3)
    df["rolling_std"] = df["return_1"].rolling(5).std()
    df["volume_spike"] = df["volume"] / df["volume"].rolling(10).mean()
    df["price_above_ema"] = (df["close"] > df["ema_21"]).astype(int)
    df["rsi_oversold"] = (df["rsi"] < 30).astype(int)
    df["macd_cross_up"] = ((df["macd_diff"] > 0) & (df["macd_diff"].shift(1) < 0)).astype(int)
    df["volatility"] = df["high"] - df["low"]
    df["momentum_3"] = df["close"] - df["close"].shift(3)
    return df

def predict(df):
    df = df.dropna().copy()
    if len(df) == 0:
        return 1, 0.0 

    X = df[FEATURES].iloc[-1:] 

    xgb_proba = models[0].predict_proba(X)[0]
    lgbm_proba = models[1].predict_proba(X)[0]
    rf_proba = models[2].predict_proba(X)[0]

    weights = [0.4, 0.35, 0.25]
    weighted_proba = (
        weights[0] * xgb_proba +
        weights[1] * lgbm_proba +
        weights[2] * rf_proba
    )

    final_class = int(np.argmax(weighted_proba)) 
    confidence = float(np.max(weighted_proba))

    return final_class, confidence

def log_trade(symbol, entry, exit, pnl):
    trade = pd.DataFrame([[symbol, entry, exit, pnl]], columns=["Symbol", "Entry", "Exit", "PnL"])
    trade.to_csv("logs/trades.csv", mode="a", index=False, header=not pd.io.common.file_exists("logs/trades.csv"))

    trade_json = {
        "symbol": symbol,
        "entry": entry,
        "exit": exit,
        "pnl": pnl,
        "timestamp": datetime.now().isoformat()
    }
    trades.append(trade_json)
    with open("logs/trades.json", "w") as f: 
        json.dump(trades, f)

def log_balance(timestamp, bal):
    row = pd.DataFrame([[timestamp, bal]], columns=["Timestamp", "Balance"])
    row.to_csv("logs/balance.csv", mode="a", index=False, header=not pd.io.common.file_exists("logs/balance.csv"))

def log_signal(signal_type, confidence):
    timestamp = datetime.now().isoformat()
    signal_data = {
        "signal": "BUY" if signal_type == 1 else "SELL",
        "confidence": confidence,
        "timestamp": timestamp
    }

    try:
        if os.path.exists("logs/signals.json"):
            with open("logs/signals.json", "r") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        else:
            existing = []
    except Exception as e:
        print("❌ Error reading signals.json:", e)
        existing = []

    existing.append(signal_data)

    try:
        with open("logs/signals.json", "w") as f:
            json.dump(existing, f)
    except Exception as e:
        print("❌ Error writing signals.json:", e)

# def log_marker(signal_type, price, timestamp):
#     marker = {
#         "type": "BUY" if signal_type == 1 else "SELL",
#         "price": price,
#         "timestamp": timestamp  # should be ISO format
#     }

#     try:
#         if os.path.exists("logs/marks.json"):
#             with open("logs/marks.json", "r") as f:
#                 existing = json.load(f)
#         else:
#             existing = []
#     except:
#         existing = []

#     existing.append(marker)

#     try:
#         with open("logs/marks.json", "w") as f:
#             json.dump(existing, f)
#     except Exception as e:
#         print("❌ Failed to save marker:", e)

def run(symbol: str, timeframe:str):
    global position, entry_price, balance, quantity, entry_time

    print("🧠 Starting AI Binary Paper Trader...: \n", state.running)


    while state.running:
        try:
            df = fetch_ohlcv(symbol, timeframe)
            df = add_indicators(df)
            append_live_data(df)
            signal, confidence = predict(df)
            price = df["close"].iloc[-1]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{timestamp}] 💹 Price: {price:.2f} | Signal: {signal} | Confidence: {confidence:.2%} | Position: {position}")
            df['trend'] = df['ema_21'] > df['sma_50']

            # rsi = df['rsi'].iloc[-1]
            # macd_cross = df['macd_cross_up'].iloc[-1]

            if position is None:
                if signal == 1 and confidence > 0.52:
                    log_signal(signal, confidence)
                # log_marker(signal, price, datetime.now().isoformat)

                    position = "LONG"
                    entry_price = price
                    quantity = balance / price
                    entry_time = time.time()
                    print(f"[{timestamp}] 🟢 BUY @ {price:.2f} | Confidence: {confidence:.2%}")

            elif position == "LONG":
                unrealized_pnl = (price - entry_price) * quantity
                time_held = time.time() - entry_time

                exit_conditions = [
                    signal == 0,
                    unrealized_pnl <= -1 * df['atr'].iloc[-1] * quantity,
                    unrealized_pnl >= 2 * df['atr'].iloc[-1] * quantity,
                    time_held > 1200  # Optional: 20 minutes
                ]

                if any(exit_conditions):
                    log_signal(signal, confidence)
                    # log_marker(signal, price, datetime.now().isoformat)
                # if (exit_signal == 0 and exit_conf > 0.55) or unrealized_pnl <= stop_loss or unrealized_pnl >= take_profit:
                    # log_trade("BUY", "BTC/USDT", entry_price, 0, confidence)
                    # log_trade("SELL", "BTC/USDT", exit_price, profit, confidence)

                    pnl = unrealized_pnl
                    balance += pnl
                    log_trade(symbol, entry_price, price, pnl)
                    print(f"[{timestamp}] 🔴 SELL @ {price:.2f} | PnL: {pnl:.2f} | Held: {time_held//60:.1f} min | New Balance: {balance:.2f}")
                    position = None
                    entry_price = 0.0
                    quantity = 0
                    entry_time = None

            log_balance(timestamp, balance)

        except Exception as e:
            print("❌ Error:", e)

        time.sleep(10)


# if __name__ == "__main__":
#     run()
