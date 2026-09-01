import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_solar_forecaster(df: pd.DataFrame):
    """
    Trains an XGBoost regressor for Berlin solar PV power forecasting 
    using chronological splitting and weather features.
    """
    features = ['solar_zenith_angle', 'wind_speed', 'temperature', 'wind_lag_east']
    target = 'pv_generation_mw'
    
    X = df[features]
    y = df[target]
    
    # Chronological split to prevent data leakage (first 80% train, last 20% test)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    model = XGBRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=5,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    return model, mae, predictions
