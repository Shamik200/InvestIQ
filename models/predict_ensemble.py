# import joblib
# import numpy as np
# import pandas as pd

# # Load tuned binary classifier models
# xgb_model = joblib.load("models/xgb_clf_tuned.pkl")
# lgbm_model = joblib.load("models/lgbm_clf_tuned.pkl")
# rf_model   = joblib.load("models/rf_clf_tuned.pkl")

# def predict_ensemble(row: pd.Series):
#     X = row.values.reshape(1, -1)

#     # Predict class probabilities
#     xgb_proba = xgb_model.predict_proba(X)[0]
#     lgbm_proba = lgbm_model.predict_proba(X)[0]
#     rf_proba = rf_model.predict_proba(X)[0]

#     # Model weights (tune as needed)
#     weights = [0.4, 0.35, 0.25]

#     # Weighted average of class 1 (BUY) probability
#     buy_prob = (
#         weights[0] * xgb_proba[1] +
#         weights[1] * lgbm_proba[1] +
#         weights[2] * rf_proba[1]
#     )

#     # Threshold for deciding to BUY
#     final_class = int(buy_prob > 0.6)
#     return final_class, buy_prob

# if __name__ == "__main__":
#     import pandas as pd

#     # Example usage
#     df = pd.read_csv("data/BTCUSDT_5m_ML_ready.csv")
#     FEATURES = [
#         'rsi', 'macd', 'macd_signal', 'macd_diff',
#         'sma_50', 'ema_21', 'atr', 'body', 'upper_wick', 'lower_wick',
#         'return_1', 'return_3', 'rolling_std', 'volume_spike'
#     ]
#     row = df[FEATURES].dropna().iloc[-1]
#     signal, conf = predict_ensemble(row)
#     print(f"Signal: {'BUY' if signal == 1 else 'NOT BUY'} | Confidence: {conf:.2%}")
