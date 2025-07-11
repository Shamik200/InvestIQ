import pandas as pd

def append_live_data(df):
    df.tail(1).to_csv(
        "data/live_collected_data.csv",
        mode="a",
        index=False,
        header=not pd.io.common.file_exists("data/live_collected_data.csv")
    )
