import pandas as pd
import ta
import numpy as np

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Add RSI
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()

    # Add MACD
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    # Add SMA and EMA
    df['sma_50'] = ta.trend.SMAIndicator(close=df['close'], window=50).sma_indicator()
    df['ema_21'] = ta.trend.EMAIndicator(close=df['close'], window=21).ema_indicator()

    # True Range & ATR
    df['atr'] = ta.volatility.AverageTrueRange(
        high=df['high'], low=df['low'], close=df['close'], window=14
    ).average_true_range()

    # Candle pattern info
    df['body'] = (df['close'] - df['open']).abs()
    df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
    df['lower_wick'] = df[['close', 'open']].min(axis=1) - df['low']

    # Price returns
    df['return_1'] = df['close'].pct_change(1)
    df['return_3'] = df['close'].pct_change(3)

    # Volatility estimate
    df['rolling_std'] = df['close'].rolling(window=10).std()

    # Volume spikes
    df['volume_rolling'] = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = (df['volume'] > 1.5 * df['volume_rolling']).astype(int)

    df["price_above_ema"] = (df["close"] > df["ema_21"]).astype(int)
    df["rsi_oversold"] = (df["rsi"] < 30).astype(int)
    df["macd_cross_up"] = ((df["macd_diff"] > 0) & (df["macd_diff"].shift(1) < 0)).astype(int)
    df["volatility"] = df["high"] - df["low"]
    df["momentum_3"] = df["close"] - df["close"].shift(3)

    return df
