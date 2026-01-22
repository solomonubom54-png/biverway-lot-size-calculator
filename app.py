import streamlit as st

# Page config
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# Header
st.title("Biverway | Lot Size Calculator")
st.write("This app calculates lot size and take profit based on the Biverway Trading System.")

# -----------------
# INPUTS
# -----------------

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

# -----------------
# CALCULATIONS
# -----------------

# Calculate Direction
direction = "BUY" if entry > sl else "SELL"

# Calculate Price Difference (points)
if symbol == "XAUUSD":
    point = abs(entry - sl) * 100
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

# Prevent division by zero
if point == 0:
    st.warning("Entry price and Stop Loss are too close or identical. Adjust them.")
    lot_size = 0
    tp = entry
else:
    # Calculate Lot Size
    if symbol == "USDCHF":
        lot_size = (risk * entry) / point
    else:
        lot_size = risk / point
    lot_size = round(lot_size, 2)

    # Calculate Take Profit (1:3)
    if symbol == "XAUUSD":
        tp_distance = abs(entry - sl) * 3
    else:
        tp_distance = (point * 3) / 100000

    tp = entry + tp_distance if direction == "BUY" else entry - tp_distance
    tp = round(tp, 5)

# -----------------
# OUTPUT
# -----------------
st.subheader("Results")
st.write("**Direction:**", direction)
st.write("**Price Diff (points):**", point)
st.write("**Lot Size:**", lot_size)
st.write("**Take Profit (1:3):**", tp)

# -----------------
# FOOTER NOTE
# -----------------
st.write("")
st.write("*Designed according to the Biverway Trading System. Risk-based lot sizing. Educational use only.*")
