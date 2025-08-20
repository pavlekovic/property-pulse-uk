import streamlit as st
import pandas as pd
import altair as alt
from config.streamlit_config import MART_FACT_BY_DISTRICT

st.title("Price Tracker")

@st.cache_data
def load_yearly():
    df = pd.read_parquet(MART_FACT_BY_DISTRICT)
    # ensure numeric
    for c in ("year", "avg_price"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

df = load_yearly()

years = sorted(df["year"].dropna().unique().tolist())
districts = sorted(df["district"].dropna().unique().tolist() if "district" in df.columns
                   else df["district_name"].dropna().unique().tolist())

with st.sidebar:
    st.subheader("Filters")
    year_min, year_max = int(min(years)), int(max(years))
    year_range = st.slider("Years", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    chosen = st.multiselect("Districts (max 10)", districts, default=districts[:5], max_selections=10)

name_col = "district" if "district" in df.columns else "district_name"
mask = (
    df["year"].between(year_range[0], year_range[1]) &
    df[name_col].isin(chosen)
)
plot_df = df.loc[mask].sort_values([name_col, "year"])

chart = (
    alt.Chart(plot_df)
    .mark_line(interpolate="monotone", strokeWidth=3)   # <-- smooth & thick
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("avg_price:Q", title="Average Price (£)"),
        color=alt.Color(f"{name_col}:N", title="District"),
        tooltip=[name_col, "year", "avg_price"]
    )
    .properties(height=600)
)

st.altair_chart(chart, use_container_width=True)