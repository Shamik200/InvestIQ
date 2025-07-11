import ccxt
import pandas as pd
import ta
import joblib

exchange = ccxt.binance()

FEATURES = [...]  # Same as your tradingbot feature list

def get_ohlcv(symbol, timeframe):
    df = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(df, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def add_indicators(df):
    # Add same indicators from papertrader here
    return df

def get_prediction(symbol, timeframe, model_type):
    df = get_ohlcv(symbol, timeframe)
    df = add_indicators(df)
    df = df.dropna()
    X = df[FEATURES].iloc[-1:]

    if model_type == "ml":
        model = joblib.load("models/xgb_clf_tuned.pkl")
    else:
        return {"error": "RL not yet supported"}

    proba = model.predict_proba(X)[0]
    final_class = int(proba.argmax())
    confidence = float(proba.max())
    return {"signal": final_class, "confidence": confidence}

def get_chart_data(symbol, timeframe):
    df = get_ohlcv(symbol, timeframe)
    return df.tail(100).to_dict(orient="records")
