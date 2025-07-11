import pandas as pd
import os

def append_live_data(df):
    df.tail(1).to_csv("data/live_collected_data.csv", mode="a", index=False, header=not os.path.exists("data/live_collected_data.csv"))
