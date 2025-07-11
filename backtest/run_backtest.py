import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backtest.backtest_simple import backtest_strategy

# Load the signals data
df = pd.read_csv('data/BTCUSDT_5m_signals.csv', parse_dates=['timestamp'])

# Run the backtest
final_balance, trades = backtest_strategy(df)

print(f"\nInitial Balance: $1000")
print(f"Final Balance: ${final_balance:.2f}")
print("\nTrade History:\n")
print(trades.tail())