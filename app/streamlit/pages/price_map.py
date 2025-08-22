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
    
    # Show property type as buttons
    if "ptype" not in st.session_state:
        st.session_state.ptype = "All"
    if "trigger_rerun" not in st.session_state:
        st.session_state.trigger_rerun = False

    def make_selector(code: str, label: str):
        is_selected = (st.session_state.ptype == code)
        if st.button(label, key=f"ptype_{code}", type=("primary" if is_selected else "secondary")):
            st.session_state.ptype = code
            st.session_state.trigger_rerun = True   # flag for rerun

    options = [
        ("All", "🔎 All"),
        ("D",   "🏡 Detached"),
        ("S",   "🏘️ Semi-Detached"),
        ("T",   "🏚️ Terraced"),
        ("F",   "🏢 Flat"),
    ]

    for code, label in options:
        make_selector(code, label)

    # Safe rerun outside callbacks → no warning
    if st.session_state.trigger_rerun:
        st.session_state.trigger_rerun = False
        st.rerun()

    property_filter = st.session_state.ptype

    # Choice of colors
    #palette_choice = st.radio("Color scheme", ["Blue", "Green", "Red"], index=0, horizontal=True)

# Filter data for year and property type
if property_filter != "All":
    sub = df[(df["year"] == year_filter) & (df["property_type"] == property_filter)].copy()
else:
    sub = df[df["year"] == year_filter].copy()

# Guard: if no rows after filtering, stop early
if sub.empty:
    st.warning("No data for the selected year/property type.")
    st.stop()

# Normalise district names (no SettingWithCopyWarning)
sub.loc[:, "__norm"] = sub["district"].map(normalize_name)

print(sub)

# Build lookup (round safely, drop NaNs)
sub_nonnull = sub.dropna(subset=["avg_price", "__norm"]).copy()
lookup = dict(zip(sub_nonnull["__norm"], sub_nonnull["avg_price"].round(0)))

#print(f"lookup: {lookup}")

# Load geo data
geojson = load_geojson()
name_field = detect_name_field(geojson, level="Local Authorities")  # Local Authorities, can be changed to postal code


print(name_field)

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