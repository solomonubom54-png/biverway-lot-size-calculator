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
risk = st.number_input("Risk Amount", format="%.2f")

inputs_ready = entry > 0 and sl > 0 and risk > 0 and entry != sl

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = abs(entry - sl) * 100
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

lot = "0.00"
actual_risk = "0.00"
tp_display = format(entry, ".3f" if symbol == "XAUUSD" else ".5f")

if inputs_ready and point > 0:

    # ---- LOT SIZE (ROUNDED FIRST) ----
    if symbol == "USDCHF":
        lot_raw = (risk * entry) / point
    else:
        lot_raw = risk / point

    lot_rounded = round(lot_raw, 2)
    lot = f"{lot_rounded:.2f}"

    # ---- ACTUAL RISK (CORRECT FORMULA) ----
    if symbol == "USDCHF":
        actual_risk_val = lot_rounded * point / entry
    else:
        actual_risk_val = lot_rounded * point

    actual_risk = f"{actual_risk_val:.2f}"

    # ---- TAKE PROFIT ----
    if symbol == "XAUUSD":
        tp_dist = abs(entry - sl) * 3
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".3f")
    else:
        tp_dist = (point * 3) / 100000
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".5f")

# ---------- RESULTS ----------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

rows = f"""
<tr><td class="result-label">Direction</td><td class="result-value">{direction}</td></tr>
"""

if inputs_ready:
    rows += f"""
<tr><td class="result-label">Actual Risk</td><td class="result-value">{actual_risk}</td></tr>
"""

rows += f"""
<tr><td class="result-label">Lot Size</td><td class="result-value">{lot}</td></tr>
<tr><td class="result-label">Take Profit (1:3)</td><td class="result-value">{tp_display}</td></tr>
"""

st.markdown(f"""
<table class="result-table">
{rows}
</table>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-note">Designed according to Biverway Trading System</div>',
    unsafe_allow_html=True
        )
