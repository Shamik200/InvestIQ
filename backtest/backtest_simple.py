import pandas as pd

def backtest_strategy(df: pd.DataFrame, initial_balance: float = 1000.0, trade_amount_pct: float = 0.1):
    df = df.copy()
    balance = initial_balance
    position = 0
    trade_log = []

    for i in range(1, len(df)):
        price = df.loc[i, 'close']
        timestamp = df.loc[i, 'timestamp']

        # Buy logic
        if df.loc[i, 'buy_signal'] and position == 0:
            qty = (balance * trade_amount_pct) / price
            balance -= qty * price
            position += qty
            trade_log.append((timestamp, 'BUY', price, balance, position))

        # Sell logic
        elif df.loc[i, 'sell_signal'] and position > 0:
            balance += position * price
            trade_log.append((timestamp, 'SELL', price, balance, 0))
            position = 0

    # Final valuation
    if position > 0:
        final_price = df.iloc[-1]['close']
        balance += position * final_price
        position = 0

    return balance, pd.DataFrame(trade_log, columns=['timestamp', 'action', 'price', 'balance', 'position'])
