import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- TITLE ----------------
st.markdown(
    "<h2 style='text-align:center; color:#f7931a;'>Biverway | Lot Size Calculator</h2>",
    unsafe_allow_html=True
)

st.write(
    "This app calculates lot size and take profit based on the Biverway Trading System."
)

# ---------------- INPUTS ----------------
st.markdown("### Inputs")

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Symbol")
with col2:
    symbol = st.selectbox(
        "",
        ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
        label_visibility="collapsed"
    )

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Entry Price")
with col2:
    entry_price = st.number_input(
        "",
        value=0.00000,
        format="%.5f",
        label_visibility="collapsed"
    )

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Stop Loss")
with col2:
    stop_loss = st.number_input(
        "",
        value=0.00000,
        format="%.5f",
        label_visibility="collapsed"
    )

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Risk Amount")
with col2:
    risk_amount = st.number_input(
        "",
        value=1.00,
        min_value=0.01,
        format="%.2f",
        label_visibility="collapsed"
    )

# ---------------- CALCULATIONS ----------------
direction = "-"
price_diff = 0
lot_size = 0
take_profit = 0

if entry_price != stop_loss:
    direction = "BUY" if entry_price > stop_loss else "SELL"

    price_diff = abs(entry_price - stop_loss)

    # Point calculation
    if symbol == "XAUUSD":
        point = price_diff * 100
        lot_size = risk_amount / point if point != 0 else 0
        take_profit = entry_price + (price_diff * 3) if direction == "BUY" else entry_price - (price_diff * 3)
    else:
        point = price_diff * 10000
        lot_size = risk_amount / point if point != 0 else 0
        take_profit = entry_price + (price_diff * 3) if direction == "BUY" else entry_price - (price_diff * 3)

else:
    st.warning("Entry price and Stop Loss are too close or identical. Adjust them.")

# ---------------- RESULTS ----------------
st.markdown("""
<style>
.result-table {
    width:100%;
    border-collapse:collapse;
    margin-top:8px;
}
.result-table td {
    border:1px solid #ccc;
    padding:8px;
    font-size:14px;
}
.result-label {
    background:#f5f5f5;
    font-weight:bold;
    width:45%;
}
.result-value {
    background:#ffffff;
    text-align:right;
}
.result-header {
    background:#d9edf7;
    padding:6px;
    font-weight:bold;
    margin-top:16px;
    border-radius:4px;
}
</style>

<div class="result-header">Results</div>

<table class="result-table">
<tr>
    <td class="result-label">Direction</td>
    <td class="result-value">{}</td>
</tr>
<tr>
    <td class="result-label">Price Diff (points)</td>
    <td class="result-value">{:.2f}</td>
</tr>
<tr>
    <td class="result-label">Lot Size</td>
    <td class="result-value">{:.2f}</td>
</tr>
<tr>
    <td class="result-label">Take Profit (1:3)</td>
    <td class="result-value">{}</td>
</tr>
</table>
""".format(
    direction,
    point if entry_price != stop_loss else 0,
    lot_size,
    f"{take_profit:.5f}" if symbol != "XAUUSD" else f"{take_profit:.2f}"
), unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center; font-size:12px; color:gray;'>"
    "Designed according to the Biverway Trading System. "
    "Risk-based lot sizing. Educational use only."
    "</p>",
    unsafe_allow_html=True
         )
