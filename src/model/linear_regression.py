# scripts/train_lin_trend.py
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

# Paths
PRED_BASE_PATH = Path("data/marts/fact_prediction")  # parquet with: price, year, district, property_type, new_build, tenure
ARTIFACT_PATH  = Path("models/lintrend_params.pkl")
ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)

def fit_log_trend(y: pd.Series, x: pd.Series):
    """Fit log(price)=a+b*year; return (a, b, rmse_log) or None if <3 pts."""
    x = x.astype(int).to_numpy()
    y = np.log(y.astype(float).to_numpy())
    if len(x) < 3:
        return None
    b, a = np.polyfit(x, y, 1)     # polyfit returns [slope, intercept]
    y_hat = a + b * x
    rmse = float(np.sqrt(np.mean((y - y_hat) ** 2)))
    return float(a), float(b), rmse

def main():
    df = pd.read_parquet(PRED_BASE_PATH)
    df = df.loc[:, ["price", "year", "district", "property_type", "new_build", "tenure"]].dropna()
    df["year"]  = df["year"].astype(int)
    df["price"] = df["price"].astype(float)
    df = df[df["year"] >= 2010]

    # Keep vocab for Streamlit selectors
    cats = {
        "district":       sorted(df["district"].astype(str).unique().tolist()),
        "property_type":  sorted(df["property_type"].astype(str).unique().tolist()),
        "new_build":      sorted(df["new_build"].astype(str).unique().tolist()),
        "tenure":         sorted(df["tenure"].astype(str).unique().tolist()),
    }

    params = {}
    for key, g in df.groupby(["district", "property_type", "new_build", "tenure"], sort=False):
        yearly = (g.groupby("year", as_index=False)["price"].mean()
                    .dropna().sort_values("year"))
        fit = fit_log_trend(yearly["price"], yearly["year"])
        if not fit:
            continue
        a, b, s = fit
        last_year = int(yearly["year"].max())
        mu_last   = float(np.exp(a + b * last_year))  # model-implied level at last obs year
        params[tuple(map(str, key))] = {
            "a": a, "b": b, "rmse_log": s, "last_year": last_year, "mu_last": mu_last
        }

    artifact = {
        "params": params,
        "cat_categories": cats,
        "year_max": int(df["year"].max()),
    }
    joblib.dump(artifact, ARTIFACT_PATH)
    print(f"[train] saved → {ARTIFACT_PATH}  (segments: {len(params)})")

if __name__ == "__main__":
    main()