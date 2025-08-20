import streamlit as st
import pandas as pd
import altair as alt
from config.streamlit_config import MART_FACT_BY_DISTRICT

st.title("Price Tracker")

# Cache data so that Streamlit does not load on every run
@st.cache_data
def load_yearly():
    df = pd.read_parquet(MART_FACT_BY_DISTRICT)
    # ensure numeric
    for c in ("year", "avg_price"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

df = load_yearly()

# Define a list of years for slider
years = sorted(df["year"].dropna().unique().tolist())

# Define list of districts for the dropdown
districts = sorted(df["district"].dropna().unique().tolist())

# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    year_min, year_max = int(min(years)), int(max(years))
    
    # Show year slider
    year_range = st.slider("Years", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    
    # Show dropdown box
    chosen = st.multiselect("Districts (max 5)", districts, default=None, max_selections=5)

name_col = "district"

mask = (
    df["year"].between(year_range[0], year_range[1]) &
    df["district"].isin(chosen)
)

plot_df = df.loc[mask].sort_values(["district", "year"])

chart = (
    alt.Chart(plot_df)
    .mark_line(interpolate="monotone", strokeWidth=3)   # <-- smooth & thick
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("avg_price:Q", title="Average Price (£)"),
        color=alt.Color(f"{name_col}:N", title="District"),
        tooltip=["district", "year", "avg_price"]
    )
    .properties(height=600)
)

st.altair_chart(chart, use_container_width=True)