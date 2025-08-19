import streamlit as st

st.set_page_config(page_title="Property Pulse UK", layout="wide")

st.title("Property Pulse UK")
st.write("""
Welcome! Use the pages on the left:
- **Price Tracker**: compare localities over time.
- **Map**: choropleth of average prices by locality.
- **Price Prediction**: simple starter model to estimate future prices.
""")