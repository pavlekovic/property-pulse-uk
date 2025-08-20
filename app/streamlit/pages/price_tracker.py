import streamlit as st
import pandas as pd
from app.streamlit.lib.viz import price_lines
from app.streamlit.lib.io import load_fact_by_district

st.title("Price Tracker")
st.set_page_config(page_title="Price Tracker", layout="wide")

# Load data
df = load_fact_by_district()

# Define a list of years for slider
years = sorted(df["year"].dropna().unique().tolist())

# Define a a list of property types to choose from
property_filter = sorted(df["property_type"].dropna().unique()) + ["All"]

# Define list of districts for the dropdown
districts = sorted(df["district"].dropna().unique().tolist())

# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    year_min, year_max = int(min(years)), int(max(years))
    
    # Show year slider
    year_range = st.slider("Years", min_value=year_min, max_value=year_max, value=(year_min, year_max))
    
    # Show property selector
    property_types = st.radio("Property type", property_filter, horizontal=True)
    
    # Show dropdown box for districts
    district_filter = st.multiselect("Districts (max 5)", districts, max_selections=5)

mask = (
    df["year"].between(year_range[0], year_range[1]) &
    df["district"].isin(district_filter) &
    (df["property_type"] == property_types)
)

plot_df = df.loc[mask].sort_values(["district", "year"])

if plot_df.empty:
    st.info("Select at least one district.")
else:
    chart = price_lines(plot_df, name_col="district")
    st.altair_chart(chart, use_container_width=True)