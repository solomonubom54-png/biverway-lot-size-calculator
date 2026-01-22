import streamlit as st

st.set_page_config(page_title="Biverway | Lot Size Calculator", layout="centered")

st.markdown("""
<style>
.header {
    background:#f5a623;
    padding:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
}
.section {
    background:#eeeeee;
    padding:6px;
    font-weight:bold;
    border-radius:4px;
    margin-top:12px;
}
.result {
    background:#eef6ff;
    padding:8px;
    border-radius:4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------- INPUTS ----------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])
    entry = st.number_input("Entry Price", format="%.5f")
with col2:
    sl = st.number_input("Stop Loss", format="%.5f")
    risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f")

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = round(abs(entry - sl) * 100, 1)
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

if point == 0:
    lot = 0
    tp = entry
else:
    if symbol == "USDCHF":
        lot = round((risk * entry) / point, 2)
    else:
        lot = round(risk / point, 2)

    tp_distance = abs(entry - sl) * 3 if symbol == "XAUUSD" else (point * 3) / 100000
    tp = round(entry + tp_distance if direction == "BUY" else entry - tp_distance, 5)

# ---------- RESULTS ----------
st.markdown('<div class="section" style="background:#d9edf7;">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="result"><b>Direction:</b> {direction}</div>
<div class="result"><b>Price Diff (points):</b> {point}</div>
<div class="result"><b>Lot Size:</b> {lot}</div>
<div class="result"><b>Take Profit (1:3):</b> {tp}</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color:gray;font-size:12px;margin-top:10px;">
Designed according to the Biverway Trading System.<br>
Risk-based lot sizing. Educational use only.
</div>
""", unsafe_allow_html=True)
