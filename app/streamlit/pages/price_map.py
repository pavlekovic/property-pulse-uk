import streamlit as st
import pydeck as pdk
from app.streamlit.lib.io import load_fact_by_district, load_geojson
from app.streamlit.lib.geo import detect_name_field, normalize_name, attach_values
from app.streamlit.lib.colors import assign_colors_quantiled, color_scale_quantiles

# Define page name and title
st.title("Price Map")
st.set_page_config(page_title="Price Map", layout="wide")

# Load data
df = load_fact_by_district()

# Define a list of years for dropdown menu
years = sorted(df["year"].dropna().unique().tolist(), reverse=True)

# Define a list of districts
districts = sorted(df["district"].dropna().unique())

# Define a list of property types
types =  sorted(df["property_type"].dropna().unique())


# Define mapping: internal code → user-friendly label
ptype_map = {
    "All": "All",
    "D": "Detached",
    "S": "Semi-Detached",
    "T": "Terraced",
    "F": "Flat"
}

# Reverse map (label → code)
ptype_reverse = {v: k for k, v in ptype_map.items()}


# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    
    # Show year dropdown
    year_filter = st.selectbox("Year", years)
    
    # Show property selector
    ptype_label = st.radio("Property type", list(ptype_map.values()), horizontal=True)
    # Convert back to internal code for filtering
    property_filter = ptype_reverse[ptype_label]

    # --- inside your existing "with st.sidebar:" block, after property_filter ---
    palette_choice = st.radio("Color scheme", ["Blue", "Green", "Red"], index=0, horizontal=True)

# Filter data for year and property type
if property_filter != "All":
    sub = df[(df["year"] == year_filter) & (df["property_type"] == property_filter)]
else:
    sub = df[df["year"] == year_filter]

# Build lookup: district (normalized)
sub["__norm"] = sub["district"].map(normalize_name)
lookup = dict(zip(sub["__norm"], round(sub["avg_price"],0)))

# Load geo data
geojson = load_geojson()
name_field = detect_name_field(geojson, level="Local Authorities")  # Local Authorities, can be changed to postal code

# Match values from sub (price data) to geojson
matched_values = attach_values(geojson, lookup, name_field, value_field="avg_price")

# Build quantile scale
edges, colors = color_scale_quantiles(matched_values, n_bins=6, rgb_col=palette_choice.lower())

# Assign colors to features
assign_colors_quantiled(geojson, value_field="avg_price", edges=edges, colors=colors)

# Default view
view_state = pdk.ViewState(latitude=53.0, longitude=-3.0, zoom=5.7, bearing=0, pitch=0)

# Render geo layer
layer = pdk.Layer(
    "GeoJsonLayer",
    geojson,
    get_fill_color="properties.fill_rgba",
    get_line_color=[80, 80, 80, 120],
    line_width_min_pixels=0.5,
    pickable=True,
    stroked=True,
    filled=True,
    auto_highlight=True,
)

tooltip = {"html": "<b>{__display_name}</b><br/>Avg price: £{avg_price}",
           "style": {"backgroundColor": "rgba(30,30,30,0.85)", "color": "white"}}

st.pydeck_chart(
    pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip, map_style="light-v9"),
    use_container_width=True,
    height=800
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