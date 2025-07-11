import pandas as pd

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['buy_signal'] = (
        (df['rsi'] < 40) &
        (df['macd_diff'] > 0)
    )

    df['sell_signal'] = (
        (df['rsi'] > 60) &
        (df['macd_diff'] < 0)
    )

    return df
