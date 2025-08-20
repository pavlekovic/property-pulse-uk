import json
import pandas as pd
import streamlit as st
from config.streamlit_config import MART_FACT_BY_TYPE, GEOJSON_PATH

# Make sure to cache results for better performance
@st.cache_data
def load_fact_by_district(columns=("district", "year", "avg_price", "property_type")) -> pd.DataFrame:
    """Load the district-level mart."""
    
    # Read parquet file
    df = pd.read_parquet(MART_FACT_BY_TYPE, columns=list(columns))
    
    # ensure types
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")                 # Ensure int
    if "avg_price" in df.columns:
        df["avg_price"] = pd.to_numeric(df["avg_price"], errors="coerce")       # Ensure int
    if "district" in df.columns:
        df["district"] = df["district"].astype(str).str.strip()                 # Ensure str, remove space
    if "property_type" in df.columns:
        df["property_type"] = df["property_type"].astype(str).str.strip()       # Ensure str, remove space
        
    return df.dropna(subset=["district", "year", "avg_price"])

# Make sure to cache results for better performance
@st.cache_data
def load_geojson(path: str | None = None) -> dict:
    """Load GeoJSON data."""
    
    gj_path = GEOJSON_PATH
    with open(gj_path, "r", encoding="utf-8") as f:
        return json.load(f)