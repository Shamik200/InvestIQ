import pandas as pd
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
import joblib
from prepare_ml_data import create_labels
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
import json


def tune_xgb(data_path: str):
    df = pd.read_csv(data_path)
    df.dropna(inplace=True)

    # ✅ Create binary label
    df = create_labels(df)

    print("Original label distribution:")
    print(df['label'].value_counts(normalize=True))

    features = [
        'rsi', 'macd', 'macd_signal', 'macd_diff',
        'sma_50', 'ema_21', 'atr', 'body', 'upper_wick', 'lower_wick',
        'return_1', 'return_3', 'rolling_std', 'volume_spike',
        'price_above_ema', 'rsi_oversold', 'macd_cross_up',
        'volatility', 'momentum_3'
    ]

    X = df[features]
    y = df['label']

    # ✅ Split before balancing (no shuffle to preserve time order)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    # ✅ Balance training data
    over = SMOTE(sampling_strategy=0.5)  # 1s will be 50% of 0s
    under = RandomUnderSampler(sampling_strategy=0.8)  # 0s will be 80% of new 1s
    pipeline = Pipeline(steps=[('o', over), ('u', under)])

    X_train_bal, y_train_bal = X_train, y_train

    print("Balanced label distribution (training):")
    print(pd.Series(y_train_bal).value_counts(normalize=True))

    # ✅ No need for scale_pos_weight if balanced!
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')

    param_grid = {
        'n_estimators': [100],
        'max_depth': [3, 5],
        'learning_rate': [0.1],
    }

    grid = GridSearchCV(
        model,
        param_grid,
        scoring='accuracy',
        cv=3,
        verbose=1,
        n_jobs=-1
    )
    print("✅ Test set label distribution:")
    print(y_test.value_counts())

    grid.fit(X_train_bal, y_train_bal)
    print("Test Accuracy:", accuracy_score(y_test, grid.predict(X_test)))
    print("Predictions on test set:")
    print(pd.Series(grid.predict(X_test)).value_counts(normalize=True))
    
    best_model = grid.best_estimator_

    # ✅ Show test performance
    print("Test set performance:")
    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(best_model, "models/xgb_clf_tuned.pkl")
    print("✅ XGBoost model saved.")

if __name__ == "__main__":
    tune_xgb("data/BTCUSDT_1m_with_indicators_ML_ready.csv")
