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
types =  sorted(df["property_type"].dropna().unique()) + ["All"]

# Sidebar filters
with st.sidebar:
    st.subheader("Filters")
    
    # Show year dropdown
    year_filter = st.selectbox("Year", years)
    
    # Show property selector
    property_filter = st.radio("Property type", types, horizontal=True)

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
edges, colors = color_scale_quantiles(matched_values, n_bins=6)

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
    pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip, map_style=None),
    use_container_width=True,
    height=800
)