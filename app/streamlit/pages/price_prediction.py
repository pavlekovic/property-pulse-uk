import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(page_title="Price Prediction", layout="wide")
st.title("Price Prediction")

# Artifacts / data
MODEL_PATH = Path("models/xgb_price.pkl")              # only used to load category vocab
PRED_BASE_PATH = Path("data/marts/fact_prediction")    # parquet with columns at least:
                                                       # price, year, district, property_type, new_build, tenure

# ---------- Helpers ----------
@st.cache_resource
def load_artifact():
    """Load trained XGB artifact to reuse category vocab for UI selections."""
    art = joblib.load(MODEL_PATH)
    return {
        "cat_categories": art["cat_categories"],   # dict of vocab for district / property_type / new_build / tenure
        "year_max": int(art.get("year_max", 2024))
    }

@st.cache_data
def load_pred_base() -> pd.DataFrame:
    """Read the base mart with individual transactions (or already aggregated to row-level),
       and ensure basic types."""
    df = pd.read_parquet(PRED_BASE_PATH)
    df = df.loc[:, ["price", "year", "district", "property_type", "new_build", "tenure"]].copy()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    for c in ["district", "property_type", "new_build", "tenure"]:
        df[c] = df[c].astype(str)
    # Keep 2010+ as you requested
    df = df[df["year"] >= 2010]
    return df.dropna(subset=["price", "year"])

def compute_logtrend_forecast(df_seg: pd.DataFrame, horizon: int = 5):
    """
    Fit log(price) ~ a + b*year on the segment's historical *average* prices.
    Return forecast path for next `horizon` years (absolute, not anchored).
    Also return a simple 95% band from residual stddev in log space.
    If insufficient data (<3 points), return None to trigger fallback.
    """
    hist = (df_seg.groupby("year", as_index=False)["price"].mean()
                  .sort_values("year").dropna())
    if len(hist) < 3:
        return None

    x = hist["year"].astype(int).to_numpy()
    y = np.log(hist["price"].astype(float).to_numpy())

    # Simple linear fit in log space
    b, a = np.polyfit(x, y, 1)  # y ≈ a + b*x  (polyfit returns [slope, intercept] → we unpack as b, a)
    y_hat = a + b * x
    resid = y - y_hat
    s = float(np.sqrt(np.mean(resid**2)))  # RMSE in log space

    last_obs_year = int(hist["year"].max())
    future_years = np.arange(last_obs_year + 1, last_obs_year + 1 + horizon, dtype=int)

    # Point forecast in log space
    y_future = a + b * future_years
    mu_future = np.exp(y_future)  # convert back to price level

    # 95% band (simple, symmetric in log space)
    lower = np.exp(y_future - 1.96 * s)
    upper = np.exp(y_future + 1.96 * s)

    # NEW: model-implied level at last observed year
    mu_last = float(np.exp(a + b * last_obs_year))
    
    out = pd.DataFrame({
        "year": future_years,
        "mu": mu_future,
        "lower": lower,
        "upper": upper
    })
    return out, last_obs_year, float(s), mu_last

def anchor_to_asking(pred_df: pd.DataFrame, mu_last: float, asking_price: float) -> pd.DataFrame:
    """
    Convert absolute forecasts (mu, lower, upper) into an anchored path starting from asking_price.
    We scale by the ratio vs the model's predicted value at the last observed year.
    """
    pivot = float(pred_df["mu"].iloc[0])  # next year's model-implied mean

    ratio = pred_df["mu"] / mu_last
    ratio_lo = pred_df["lower"] / mu_last
    ratio_hi = pred_df["upper"] / mu_last

    anchored = pred_df.copy()
    anchored["pred_price"] = asking_price * ratio
    anchored["lower_95"]   = asking_price * ratio_lo
    anchored["upper_95"]   = asking_price * ratio_hi
    return anchored[["year", "pred_price", "lower_95", "upper_95"]]

# ---------- Load data & categories ----------
artifact = load_artifact()
df_base = load_pred_base()
cats = artifact["cat_categories"]

# ---------- Inputs (main page) ----------
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    district = st.selectbox("District", options=cats["district"])
with c2:
    ptype = st.selectbox("Property type", options=cats["property_type"])
with c3:
    new_build = st.radio("New build", options=cats["new_build"], horizontal=True)
with c4:
    tenure = st.radio("Tenure", options=cats["tenure"], horizontal=True)
with c5:
    asking_price = st.number_input("Asking price (£)", min_value=50_000, max_value=5_000_000, step=5_000)

st.write("---")

# ---------- Filter segment & forecast ----------
seg = df_base[
    (df_base["district"] == district) &
    (df_base["property_type"] == ptype) &
    (df_base["new_build"] == new_build) &
    (df_base["tenure"] == tenure)
].copy()

horizon = 5
res = compute_logtrend_forecast(seg, horizon=horizon)

if res is None:
    st.warning("Not enough history for this segment (need ≥ 3 yearly points). Showing flat forecast.")
    years = np.arange(int(df_base["year"].max()) + 1, int(df_base["year"].max()) + 1 + horizon, dtype=int)
    results = pd.DataFrame({
        "year": years,
        "pred_price": [asking_price] * horizon,
        "lower_95": [asking_price * 0.9] * horizon,
        "upper_95": [asking_price * 1.1] * horizon
    })
    
    # Add baseline: current year average
    baseline = pd.DataFrame({
        "year": [str(current_year)],       # last observed year (e.g., 2025)
        "pred_price": [seg_now],  # current avg for that segment
        "lower_95": [seg_now],    # no interval for historical
        "upper_95": [seg_now],
    })

    # Prepend baseline row to forecasted results
    results["year"] = results["year"].astype(str)  # make future years strings
    results = pd.concat([baseline, results], ignore_index=True)

    st.write("DEBUG preview of results:", results.head(10))
    
else:
    pred_df, last_obs_year, _, mu_last = res
    results = anchor_to_asking(pred_df, mu_last, asking_price)
    

# ---------- Plot ----------
st.subheader("Forecast (next 5 years)")
chart = (
    alt.Chart(results)
    .mark_line(color="green", strokeWidth=3, point=alt.OverlayMarkDef(color="green", size=80))
    .encode(
        x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("pred_price:Q", title="Predicted Price (£)"),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("pred_price:Q", title="Pred (£)", format=",.0f"),
            alt.Tooltip("lower_95:Q", title="Lower 95%", format=",.0f"),
            alt.Tooltip("upper_95:Q", title="Upper 95%", format=",.0f"),
        ],
    )
)

band = (
    alt.Chart(results)
    .mark_area(opacity=0.10, color="green")
    .encode(
        x="year:O",
        y="lower_95:Q",
        y2="upper_95:Q",
    )
)

st.altair_chart((band + chart).properties(height=420), use_container_width=True)

st.write("---")

# ---------- Table + metric ----------

import datetime
from app.streamlit.lib.io import load_fact_by_district
current_year = datetime.datetime.now().year

df_avg = load_fact_by_district()

# Current average for this segment
seg_now = (
    df_avg.query(
        "year == @current_year and district == @district and property_type == @ptype"
    )["avg_price"]
    .mean()
)

if pd.notna(seg_now) and seg_now > 0:
    diff_pct = (asking_price - seg_now) / seg_now * 100.0
    higher_lower = "higher" if diff_pct > 0 else "lower"
else:
    seg_now = None
    diff_pct = None

# 5-year projection (from your forecast results DataFrame)
pred_end   = float(results["pred_price"].iloc[-1])
last_year  = int(results["year"].iloc[-1])
pred_start = float(results["pred_price"].iloc[0])
growth_pct = ((pred_end / pred_start) - 1.0) * 100.0 if pred_start > 0 else None

col1, col2 = st.columns(2)

with col1:
    if seg_now is not None and diff_pct is not None and growth_pct is not None:
        grow_word = "grow" if growth_pct >= 0 else "decline"
        grow_color = "#16a34a" if growth_pct >= 0 else "#dc2626"   # green / red
        diff_color = "#16a34a" if diff_pct < 0 else "#dc2626"       # cheaper → green

        # Card container
        with st.container(border=True):   # needs Streamlit >=1.32
            st.markdown(
                f"""
                <div style="font-size:18px; font-weight:600; margin-bottom:6px;">
                  Price vs local average
                </div>
                <div style="font-size:15px; line-height:1.5; margin-bottom:12px;">
                  The current asking price <b>£{asking_price:,.0f}</b> is
                  <span style="color:{diff_color}; font-weight:700;">
                    {abs(diff_pct):.1f}% {'higher' if diff_pct > 0 else 'lower'}
                  </span>
                  than the average <b>£{seg_now:,.0f}</b> for similar properties in
                  <b>{district}</b>.
                  <br/>
                  Over the next 5 years, the value is projected to
                  <span style="color:{grow_color}; font-weight:700;">
                    {grow_word} by {abs(growth_pct):.1f}%
                  </span>
                  to <b>£{pred_end:,.0f}</b> by <b>{last_year}</b>.
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Metrics inside card
            cL, cR = st.columns(2)

            with cL:
                st.metric(
                    label="Vs segment average (now)",
                    value=f"£{asking_price:,.0f}",
                    delta=f"{+abs(diff_pct):.1f}%" if diff_pct > 0 else f"-{abs(diff_pct):.1f}%",
                    delta_color="inverse"
                )
            with cR:
                st.metric(
                    label="5-yr projection",
                    value=f"£{pred_end:,.0f}",
                    delta=f"{('+ ' if growth_pct > 0 else '')}{growth_pct:.1f}%"
                )
    else:
        st.info("Could not compute comparison or projection for this selection.")

with col2:
    st.dataframe(
        results.assign(
            pred_price=lambda d: d["pred_price"].round(0).map(lambda x: f"£{x:,.0f}"),
            lower_95=lambda d: d["lower_95"].round(0).map(lambda x: f"£{x:,.0f}"),
            upper_95=lambda d: d["upper_95"].round(0).map(lambda x: f"£{x:,.0f}"),
        ).rename(
            columns={
                "year" : "Year",
                "pred_price": "Predicted Price",
                "lower_95": "Lower 95%",
                "upper_95": "Upper 95%"
            }
            ),
        use_container_width=True,
        hide_index=True,
    )

# Copyright info
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <small>
    Contains HM Land Registry data © Crown copyright and database right 2021.  
    Licensed under 
    <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" target="_blank">
    OGL v3.0</a>.
    </small>
    """,
    unsafe_allow_html=True
)