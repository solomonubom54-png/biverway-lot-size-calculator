import streamlit as st

st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

st.title("Biverway | Lot Size Calculator")

st.write("This app will calculate lot size based on the Biverway Trading System.")

# Symbol selector
symbol = st.selectbox(
    "Select Symbol",
    ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"]
)

# Entry Price input
entry = st.number_input("Entry Price", format="%.5f")

# Stop Loss input
sl = st.number_input("Stop Loss", format="%.5f")

# Risk Amount input
risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f")

