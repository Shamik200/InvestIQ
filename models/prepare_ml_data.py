import pandas as pd

def create_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create binary classification labels:
    1 = buy (if future return > 0.1%)
    0 = sell (otherwise)
    """
    df = df.copy()
    df["label"] = (df["close"].pct_change().shift(-1) > 0).astype(int)
    return df
