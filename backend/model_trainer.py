import os
import pandas as pd
import ccxt
import subprocess
import sys

import ta

def fetch_ohlcv(symbol, timeframe):
    exchange = ccxt.binance()
    df = exchange.fetch_ohlcv(symbol, timeframe, limit=1000)
    df = pd.DataFrame(df, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    print("OHLCV")
    return df

def save_for_training(symbol, timeframe, df):
    os.makedirs("data", exist_ok=True)
    symbol_clean = symbol.replace("/", "")
    file_path = f"data/{symbol_clean}_{timeframe}_with_indicators_ML_ready.csv"
    df.to_csv(file_path, index=False)
    print("SFT")
    return file_path

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
    print("IND")
    return df

def train_all_models(symbol: str, timeframe: str):
    print(f"📊 Starting training for {symbol} ({timeframe})...")

    df = fetch_ohlcv(symbol, timeframe)
    print("✅ OHLCV data fetched.")

    df = add_indicators(df)
    print("✅ Indicators added.")

    df.dropna(inplace=True)

    timeframe = ''.join(filter(str.isdigit, timeframe))
    csv_path = save_for_training(symbol, timeframe, df)
    print(f"✅ Data saved to {csv_path}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, "models")

    print("🚀 Starting XGBoost training...")
    subprocess.run(["python", os.path.join(models_dir, "../models/tune_xgb.py"), csv_path])
    print("✅ XGBoost model trained and saved.")

    print("🚀 Starting LightGBM training...")
    subprocess.run(["python", os.path.join(models_dir, "../models/tune_lgbm.py"), csv_path])
    print("✅ LightGBM model trained and saved.")

    print("🚀 Starting Random Forest training...")
    subprocess.run(["python", os.path.join(models_dir, "../models/tune_rf.py"), csv_path])
    print("✅ Random Forest model trained and saved.")

    print("🎉 All models trained and saved successfully.")


if __name__ == "__main__":
    train_all_models("BTC/USDT", "1m")
