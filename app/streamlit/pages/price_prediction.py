# app/streamlit/pages/Price_Prediction.py
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import joblib
from pathlib import Path
import datetime
#from config.streamlit_config import ARTIFACT_PATH
from app.streamlit.lib.io import load_fact_by_district


from config.streamlit_config import ARTIFACT_PATH

# Makre sure the dir exists
ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)


st.set_page_config(page_title="Price Prediction", layout="wide")
st.title("Price Prediction")

# ---------- Load small artifact (no Parquet at runtime) ----------
@st.cache_resource
def load_artifact():
    #return joblib.load("models/lintrend_params.pkl")
    return joblib.load(ARTIFACT_PATH)

def forecast_from_params(a: float, b: float, s_log: float, last_year: int, years_ahead: int = 5) -> pd.DataFrame:
    """Absolute forecast path in price space, with simple 95% band."""
    years = np.arange(last_year + 1, last_year + 1 + years_ahead, dtype=int)
    y_log = a + b * years
    mu    = np.exp(y_log)
    lo    = np.exp(y_log - 1.96 * s_log)
    hi    = np.exp(y_log + 1.96 * s_log)
    return pd.DataFrame({"year": years, "mu": mu, "lower": lo, "upper": hi})

def anchor_to_asking(pred_df: pd.DataFrame, mu_last: float, asking_price: float) -> pd.DataFrame:
    """Scale model’s absolute path to start from asking_price (keeps shape)."""
    ratio   = pred_df["mu"]    / mu_last
    ratio_l = pred_df["lower"] / mu_last
    ratio_u = pred_df["upper"] / mu_last
    out = pred_df.copy()
    out["pred_price"] = asking_price * ratio
    out["lower_95"]   = asking_price * ratio_l
    out["upper_95"]   = asking_price * ratio_u
    return out[["year", "pred_price", "lower_95", "upper_95"]]

art = load_artifact()
params = art["params"]
cats   = art["cat_categories"]
year_max = int(art["year_max"])

# ---------- Inputs ----------
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    district = st.selectbox("District", options=["Select a district"] + cats["district"], index=0)
    district = None if district == "Select a district" else district
with c2:
    asking_price = st.number_input("Current value (£)", min_value=50_000, max_value=5_000_000, step=5_000, value=None)
with c3:
    # D/S/T/F radio with icons
    ptype_map = {"D": "Detached", "S": "Semi-Detached", "T": "Terraced", "F": "Flat"}
    icon_map  = {"D": "🏡", "S": "🏘️", "T": "🏚️", "F": "🏢"}
    labels = [f"{icon_map[k]} {v}" for k, v in ptype_map.items()]
    label_to_code = {f"{icon_map[k]} {v}": k for k, v in ptype_map.items()}
    ptype_label = st.radio("Property type", labels, horizontal=False)
    ptype = label_to_code[ptype_label]
with c4:
    nb_labels = {"N": "No", "Y": "Yes"}
    new_build_label = st.radio("New build", list(nb_labels.values()), horizontal=False)
    new_build = [k for k, v in nb_labels.items() if v == new_build_label][0]
with c5:
    ten_labels = {"F": "Freehold", "L": "Leasehold"}
    tenure_label = st.radio("Tenure", list(ten_labels.values()), horizontal=False)
    tenure = [k for k, v in ten_labels.items() if v == tenure_label][0]

if district is None or asking_price is None:
    st.info("Select a district and enter an asking price.")
    st.stop()

# ---------- Forecast ----------
key = (district, ptype, new_build, tenure)
if key not in params:
    st.warning("No history for this combination. Try another selection.")
    st.stop()

p = params[key]
pred_abs = forecast_from_params(a=p["a"], b=p["b"], s_log=p["rmse_log"], last_year=p["last_year"], years_ahead=5)
results = anchor_to_asking(pred_abs, mu_last=p["mu_last"], asking_price=asking_price)

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
      .encode(x="year:O", y="lower_95:Q", y2="upper_95:Q")
)
st.altair_chart((band + chart).properties(height=420), use_container_width=True)

st.write("---")

# ---------- “Vs average now” card + table ----------
current_year = datetime.datetime.now().year
df_avg = load_fact_by_district()

seg_now = (
    df_avg.query("year == @current_year and district == @district and property_type == @ptype")["avg_price"]
    .mean()
)

if pd.notna(seg_now) and seg_now > 0:
    diff_pct = (asking_price - seg_now) / seg_now * 100.0
else:
    seg_now = None
    diff_pct = None

pred_end   = float(results["pred_price"].iloc[-1])
last_year  = int(results["year"].iloc[-1])
pred_start = float(results["pred_price"].iloc[0])
growth_pct = ((pred_end / pred_start) - 1.0) * 100.0 if pred_start > 0 else None

col1, col2 = st.columns(2)
with col1:
    if seg_now is not None and growth_pct is not None:
        grow_word  = "grow" if growth_pct >= 0 else "decline"
        grow_color = "#16a34a" if growth_pct >= 0 else "#dc2626"
        diff_color = "#16a34a" if (diff_pct is not None and diff_pct < 0) else "#dc2626"

        with st.container(border=True):
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
            cL, cR = st.columns(2)
            with cL:
                st.metric(
                    label="Vs segment average (now)",
                    value=f"£{asking_price:,.0f}",
                    delta=f"{+abs(diff_pct):.1f}%" if diff_pct > 0 else f"-{abs(diff_pct):.1f}%",
                    delta_color="inverse",
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
        ).rename(columns={"year":"Year","pred_price":"Predicted Price","lower_95":"Lower 95%","upper_95":"Upper 95%"}),
        use_container_width=True,
        hide_index=True,
    )

# Sidebar copyright
st.sidebar.markdown(
    """
    <small>
    Contains HM Land Registry data © Crown copyright and database right.  
    Licensed under 
    <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" target="_blank">
    OGL v3.0</a>.
    </small>
    """,
    unsafe_allow_html=True
)