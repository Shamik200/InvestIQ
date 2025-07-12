import ccxt
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from indicators.indicators import add_indicators
from strategies.basic_strategy import generate_signals
from models.prepare_ml_data import create_labels
from strategies.ml_strategy import ensemble_predict_signals  # ✅ Only import this

exchange = ccxt.coinbasepro()
symbol = 'BTC/USDT'
timeframe = '1m'
limit = 1000

# Fetch OHLCV data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Add indicators
df = add_indicators(df)

# Generate ensemble ML predictions
df = ensemble_predict_signals(
    df,
    model_paths=[
        'models/xgb_clf_tuned.pkl',
        'models/lgbm_clf_tuned.pkl',
        'models/rf_clf_tuned.pkl'
    ]
)

# Create binary classification labels
df = create_labels(df)

# Save final data with indicators, signals, and labels
filename_base = f"data/{symbol.replace('/', '')}_{timeframe}"
df.to_csv(f"{filename_base}_with_indicators_ML_ready.csv", index=False)
