import joblib

def ensemble_predict_signals(df, model_paths, threshold=0.0015):
    df = df.copy()
    df.dropna(inplace=True)

    features = [
        'rsi', 'macd', 'macd_signal', 'macd_diff',
        'sma_50', 'ema_21', 'atr', 'body', 'upper_wick', 'lower_wick',
        'return_1', 'return_3', 'rolling_std', 'volume_spike',
        'price_above_ema', 'rsi_oversold', 'macd_cross_up', 'volatility', 'momentum_3'
    ]

    X = df[features]

    preds = []
    for path in model_paths:
        model = joblib.load(path)
        preds.append(model.predict(X))

    # Average predictions
    df['predicted_return'] = sum(preds) / len(preds)

    df['buy_signal'] = df['predicted_return'] > threshold
    return df
