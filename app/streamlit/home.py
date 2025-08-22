import streamlit as st
#from config.streamlit_config import GIF_PATH
from pathlib import Path

# Page configuration
st.set_page_config(page_title="PropertyPulse UK", layout="wide")

# Global global CSS
st.markdown(
    """
    <style>
      /* page width & spacing */
      .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px;}
      /* hero text */
      .hero-title {font-size: 2rem; font-weight: 700; margin: 0 0 .25rem 0;}
      .hero-sub  {color: #6b7280; margin: 0 0 1rem 0;}
      /* card look */
      .card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
      }
      .card h3 {margin: 0 0 .25rem 0; font-size: 1.1rem; font-weight: 600;}
      .card p {margin: .25rem 0 .75rem 0; color: #4b5563;}
      /* link row under hero */
      .btn-row {display: flex; gap: 10px; flex-wrap: wrap;}
      
      /* Add top spacing for the hero card */
     .hero-card {
        margin-top: 20px;   /* pushes the whole card down */
        padding-top: 10px;  /* internal spacing if you prefer */
     }
      
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ROW 1: hero (gif left)  |  intro (right)
# =========================================================

c1, c2 = st.columns([6, 6], gap="large")

st.markdown("")  # spacer

# Deployment bug - have to use path
GIF_PATH   = Path("app/streamlit/assets/map.gif")

with c1:
    if GIF_PATH.exists():
        st.image(str(GIF_PATH), width=700)
    else:
        st.info(f"No GIF at: {GIF_PATH}")

with c2:
    st.markdown(
        """
        <div class="card hero-card">
          <div class="hero-title">PropertyPulse UK</div>
          <p class="hero-sub">
            Explore HM Land Registry Price Paid data — track trends, compare areas, and project prices.
          </p>

          <h4>About the Data</h4>
          <p>
            <b>Price Paid Data</b>: Includes all property sales in England and Wales that are sold for value and 
            lodged with HM Land Registry for registration.
          </p>
          <p>
            <b>Geographic Boundaries</b>: Based on digital vector boundaries for Local Authority Districts 
            (as at May 2025), published by the ONS Geoportal.  
            We included only England and Wales in our geographic coverage.  
            Boundaries are the <i>Generalised (20m)</i> version, clipped to the coastline (Mean High Water mark).
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# ROW 2: Price Map (left) | Price Tracker (right)
# =========================================================
c3, c4 = st.columns(2, gap="large")
with c3:
    st.markdown(
        """
        <style>
          .link-btn {
            display: inline-block;
            padding: 8px 16px;
            margin-top: 8px;
            background-color: #2563eb; /* blue */
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background-color 0.2s ease;
            text-decoration: none !important;
          }
          .link-btn:hover {
            background-color: #1e40af; /* darker blue */
          }
        </style>

        <div class="card">
          <h3>Price Map</h3>
          <p>
            View average sale prices by local authority. Pick a year, choose a property type, and explore the map.
          </p>
          <a href="Price_Map" class="link-btn">Go to Price Map</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
        <style>
          .link-btn {
            display: inline-block;
            padding: 8px 16px;
            margin-top: 8px;
            background-color: #2563eb; /* blue */
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background-color 0.2s ease;
          }
          .link-btn:hover {
            background-color: #1e40af; /* darker blue */
          }
        </style>

        <div class="card">
          <h3>Price Tracker</h3>
          <p>
            Compare price trends over time. Select up to 10 districts, adjust the year range, and see the lines update.
          </p>
          <a href="Price_Tracker" class="link-btn">Go to Price Tracker</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")  # spacer

# =========================================================
# ROW 3: Price Prediction (left) | About (right)
# =========================================================
c5, c6 = st.columns(2, gap="large")
with c5:
    st.markdown(
        """
        <style>
          .link-btn {
            display: inline-block;
            padding: 8px 16px;
            margin-top: 8px;
            background-color: #2563eb; /* blue */
            color: white !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background-color 0.2s ease;
          }
          .link-btn:hover {
            background-color: #1e40af; /* darker blue */
          }
        </style>

        <div class="card">
          <h3>Price Prediction</h3>
          <p>
            Enter a district, property type, and details to see a 5-year price forecast with a simple uncertainty band.
          </p>
          <a href="Price_Prediction" class="link-btn">Go to Price Prediction</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c6:
    st.markdown(
        """
        <div class="card">
          <h3>About the data</h3>
          <p>
            Contains <a href="https://www.gov.uk/government/organisations/land-registry" target="_blank">
            HM Land Registry Price Paid data</a> © Crown copyright and database right.  
            Geographic boundary data from the <a href="https://geoportal.statistics.gov.uk/" target="_blank">
            ONS Geoportal</a> (Office for National Statistics).  
          </p>
          <p style="margin:0;">
            Both datasets are licensed under the 
            <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" target="_blank">
            Open Government Licence v3.0 (OGL)</a>.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )