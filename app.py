import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------- STYLES ----------
st.markdown("""
<style>
.header {
    background:#f5a623;
    padding:14px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:8px;
    margin-bottom:12px;
}

.section {
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    border-radius:6px;
    margin-top:14px;
    margin-bottom:8px;
}

.result-header {
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    border-radius:6px;
    margin-top:16px;
}

.result-table {
    width:100%;
    border-collapse:collapse;
    margin-top:6px;
}

.result-table td {
    border:1px solid #ccc;
    padding:10px;
    font-size:14px;
}

.result-label {
    background:#f7f7f7;
    width:50%;
}

.result-value {
    background:#eef6ff;
    font-weight:bold;
}

.footer-note {
    margin-top:22px;
    margin-bottom:40px;
    font-size:12px;
    color:#555;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------- INPUTS ----------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])

price_format = "%.3f" if symbol == "XAUUSD" else "%.5f"
entry = st.number_input("Entry Price", format=price_format)
sl = st.number_input("Stop Loss", format=price_format)
risk = st.number_input("Risk Amount", min_value=0.0, format="%.2f")

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    price_diff = abs(entry - sl)
    point = price_diff * 100
else:
    point = abs(int(entry * 100000) - int(sl * 100000))
    price_diff = point / 100000

if point == 0 or risk == 0:
    lot = "0.00"
    actual_risk = "0.00"
    tp_display = format(entry, ".3f" if symbol == "XAUUSD" else ".5f")
else:
    if symbol == "USDCHF":
        lot_value = (risk * entry) / point
    else:
        lot_value = risk / point

    lot = f"{lot_value:.2f}"

    # ----- ACTUAL RISK -----
    if symbol == "XAUUSD":
        actual_risk_value = lot_value * price_diff * 100
    else:
        actual_risk_value = lot_value * point

    actual_risk = f"{actual_risk_value:.2f}"

    # ----- TAKE PROFIT -----
    if symbol == "XAUUSD":
        tp_dist = price_diff * 3
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".3f")
    else:
        tp_dist = (point * 3) / 100000
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".5f")

# ---------- RESULTS ----------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<table class="result-table">
<tr><td class="result-label">Direction</td><td class="result-value">{direction}</td></tr>
<tr><td class="result-label">Actual Risk</td><td class="result-value">{actual_risk}</td></tr>
<tr><td class="result-label">Lot Size</td><td class="result-value">{lot}</td></tr>
<tr><td class="result-label">Take Profit (1:3)</td><td class="result-value">{tp_display}</td></tr>
</table>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-note">Designed according to Biverway Trading System</div>',
    unsafe_allow_html=True
    )
