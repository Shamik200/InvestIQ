import time
import pandas as pd
import ccxt
import ta
import joblib
from datetime import datetime

# Load tuned models
model_paths = [
    "models/xgb_tuned.pkl",
    "models/lgbm_tuned.pkl",
    "models/rf_tuned.pkl"
]
models = [joblib.load(path) for path in model_paths]

# Define features
FEATURES = [
    'rsi', 'macd', 'macd_signal', 'macd_diff',
    'sma_50', 'ema_21', 'atr', 'body', 'upper_wick', 'lower_wick',
    'return_1', 'return_3', 'rolling_std', 'volume_spike'
]

# Set threshold
THRESHOLD = 0.0015  # 0.15% return

# Initialize Binance
exchange = ccxt.binance()

def fetch_ohlcv(symbol="BTC/USDT", timeframe="1m", limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
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
    return df

def predict(df: pd.DataFrame) -> float:
    df = df.dropna().copy()
    if len(df) == 0:
        return 0.0
    latest = df.iloc[-1:]
    X = latest[FEATURES]
    preds = [model.predict(X)[0] for model in models]
    return sum(preds) / len(preds)

def run_live():
    print("🚀 Starting LIVE prediction engine...\n")
    while True:
        try:
            df = fetch_ohlcv()
            df = add_indicators(df)
            pred = predict(df)
            now = datetime.now().strftime("%H:%M:%S")
            signal = "🟢 BUY" if pred > THRESHOLD else "🔴 HOLD"
            print(f"[{now}] Predicted Return: {pred:.5f} → Signal: {signal}")
        except Exception as e:
            print("❌ Error:", e)

        time.sleep(60)  # run every minute

if __name__ == "__main__":
    run_live()
