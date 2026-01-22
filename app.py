import streamlit as st

# -----------------
# PAGE CONFIG
# -----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# -----------------
# HEADER (orange, bold, centered)
# -----------------
st.markdown(
    "<h1 style='background-color:#FFA500; color:black; padding:10px; text-align:center;'>Biverway | Lot Size Calculator</h1>",
    unsafe_allow_html=True
)
st.write("This app calculates lot size and take profit based on the Biverway Trading System.")

# -----------------
# INPUTS (2-column layout)
# -----------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<b>Symbol</b>", unsafe_allow_html=True)
with col2:
    symbol = st.selectbox("symbol_selector", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])

with col1:
    st.markdown("<b>Entry Price</b>", unsafe_allow_html=True)
with col2:
    entry = st.number_input("entry_price_input", format="%.5f")

with col1:
    st.markdown("<b>Stop Loss</b>", unsafe_allow_html=True)
with col2:
    sl = st.number_input("stop_loss_input", format="%.5f")

with col1:
    st.markdown("<b>Risk Amount</b>", unsafe_allow_html=True)
with col2:
    risk = st.number_input("risk_amount_input", min_value=1.0, format="%.2f")

# -----------------
# CALCULATIONS
# -----------------
# Direction
direction = "BUY" if entry > sl else "SELL"

# Price Difference
if symbol == "XAUUSD":
    point = round(abs(entry - sl) * 100, 1)  # Round to 1 decimal place
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

# Prevent division by zero
if point == 0:
    st.warning("Entry price and Stop Loss are too close or identical. Adjust them.")
    lot_size = 0
    tp = entry
else:
    # Lot Size
    if symbol == "USDCHF":
        lot_size = (risk * entry) / point
    else:
        lot_size = risk / point
    lot_size = round(lot_size, 2)

    # Take Profit (1:3)
    if symbol == "XAUUSD":
        tp_distance = abs(entry - sl) * 3
    else:
        tp_distance = (point * 3) / 100000

    tp = entry + tp_distance if direction == "BUY" else entry - tp_distance
    tp = round(tp, 5)

# -----------------
# OUTPUT (2-column layout like sheet)
# -----------------
st.subheader("Results")

result_labels = ["Direction", "Price Diff (points)", "Lot Size", "Take Profit (1:3)"]
result_values = [direction, point, lot_size, tp]

for label, value in zip(result_labels, result_values):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"<b>{label}</b>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"{value}", unsafe_allow_html=True)

# -----------------
# FOOTER NOTE
# -----------------
st.write("")
st.markdown(
    "<i style='color:gray;'>Designed according to the Biverway Trading System. Risk-based lot sizing. Educational use only.</i>",
    unsafe_allow_html=True
)
