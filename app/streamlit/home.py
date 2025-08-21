import streamlit as st

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        text-transform: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.set_page_config(page_title="Property Pulse UK", layout="wide")

st.title("Property Pulse UK")
st.write("""
Welcome! Use the pages on the left:
- **Price Tracker**: compare localities over time.
- **Map**: choropleth of average prices by locality.
- **Price Prediction**: simple starter model to estimate future prices.
""")