import streamlit as st

st.set_page_config(page_title="Biverway | Lot Size Calculator", layout="centered")

# ---------- STYLES ----------
st.markdown("""
<style>
.row {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    gap: 10px;
    align-items: center;
    margin-bottom: 8px;
}
.label {
    font-weight: 500;
}
.box {
    background: #eef6ff;
    padding: 6px;
    border-radius: 4px;
}
.section {
    background: #eeeeee;
    padding: 6px;
    font-weight: bold;
    border-radius: 4px;
    margin-top: 10px;
}
.header {
    background:#f5a623;
    padding:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------- INPUTS ----------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

symbol = st.selectbox("", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"], key="symbol")

entry = st.number_input("", format="%.5f", key="entry")
sl = st.number_input("", format="%.5f", key="sl")
risk = st.number_input("", min_value=1.0, format="%.2f", key="risk")

st.markdown(f"""
<div class="row"><div class="label">Symbol</div><div>{symbol}</div></div>
<div class="row"><div class="label">Entry Price</div><div>{entry:.5f}</div></div>
<div class="row"><div class="label">Stop Loss</div><div>{sl:.5f}</div></div>
<div class="row"><div class="label">Risk Amount</div><div>{risk:.2f}</div></div>
""", unsafe_allow_html=True)

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
<div class="row"><div class="label">Direction</div><div class="box">{direction}</div></div>
<div class="row"><div class="label">Price Diff (points)</div><div class="box">{point}</div></div>
<div class="row"><div class="label">Lot Size</div><div class="box">{lot}</div></div>
<div class="row"><div class="label">Take Profit (1:3)</div><div class="box">{tp}</div></div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div style="color:gray;font-size:12px;margin-top:10px;">
Designed according to the Biverway Trading System.<br>
Risk-based lot sizing. Educational use only.
</div>
""", unsafe_allow_html=True)
