import numpy as np
import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from src.utils.logging_utils import setup_logger
from config.streamlit_config import MART_PREDICTION, MODEL_PATH

# Initialize logger
logger = setup_logger(name="model", log_file="model.log")

def main():
    
    logger.info("=== MODEL TRAINING STARTED ===")
    
    # Load data
    df = pd.read_parquet(MART_PREDICTION)
    
    # Only keep relevant columns (prevention)
    logger.info("Loading data...")
    df = df.dropna(subset=["price", "year", "district", "property_type", "new_build", "tenure"]).copy()
    logger.info("Data loaded.")

    # Use a centered, compact year feature — trees split on this more readily.
    base_year = int(df["year"].min())
    df["year_rel"] = (df["year"].astype(int) - base_year).astype(int)
    
    # Cast categoricals so XGBoost can handle them natively (>=1.6) with enable_categorical=True
    for c in ["district", "property_type", "new_build", "tenure"]:
        df[c] = df[c].astype("category")

    # Features (no leakage: do NOT include price as a feature)
    feature_order = ["year_rel", "district", "property_type", "new_build", "tenure"]
    X = df[feature_order].copy()
    y = df["price"].astype(float)

    # Keep category vocab for inference
    cat_categories = {c: list(X[c].cat.categories) for c in ["district", "property_type", "new_build", "tenure"]}
    logger.info(f"Categorical features: {list(cat_categories.keys())}")

    # Train / calibration split for conformal intervals
    logger.info("Splitting train/calibration sets...")
    X_train, X_cal, y_train, y_cal = train_test_split(X, y, test_size=0.20, random_state=42)

    # Build the model
    logger.info("Training XGBoost model...")
    model = XGBRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",
        random_state=42,
        enable_categorical=True,
    )
    
    model.fit(X_train, y_train)
    logger.info("Model training complete.")
    
    # --- Conformal 90% interval (symmetric) ---
    cal_pred = model.predict(X_cal)
    resid = np.abs(y_cal - cal_pred)
    qhat = float(np.quantile(resid, 0.90))  # half-width for ~90% coverage

    logger.info(f"Conformal interval qhat={qhat:,.0f}")
    year_max = int(df["year"].max())
    logger.info(f"Min/Max year in training data: {base_year} … {year_max}")
    
    artifact = {
        "model": model,
        "feature_order": feature_order,
        "cat_categories": cat_categories,
        "qhat": qhat,
        "year_max": year_max,
        "base_year": base_year
    }
    joblib.dump(artifact, MODEL_PATH)
    
    logger.info(f"Saved model artifact → {MODEL_PATH}")
    logger.info("=== MODEL TRAINING STOPPED ===")

if __name__ == "__main__":
    main()