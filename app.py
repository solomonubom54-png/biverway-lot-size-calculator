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
    font-weight:normal;
    width:50%;
    text-align:left;
}

.result-value {
    background:#eef6ff;
    font-weight:bold;
    text-align:left;
}

.copy-section {
    margin-top:14px;
}

.footer-note {
    margin-top:20px;
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

symbol = st.selectbox(
    "Symbol",
    ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"]
)

entry = st.number_input(
    "Entry Price",
    format="%.5f"
)

sl = st.number_input(
    "Stop Loss",
    format="%.5f"
)

risk = st.number_input(
    "Risk Amount",
    min_value=1.0,
    format="%.2f"
)

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = abs(entry - sl) * 100
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

if point == 0:
    lot = 0.0
    tp = entry
else:
    if symbol == "USDCHF":
        lot = round((risk * entry) / point, 2)
    else:
        lot = round(risk / point, 2)

    tp_distance = abs(entry - sl) * 3 if symbol == "XAUUSD" else (point * 3) / 100000
    tp = round(entry + tp_distance if direction == "BUY" else entry - tp_distance, 5)

# ---------- RESULTS ----------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<table class="result-table">
<tr>
    <td class="result-label">Direction</td>
    <td class="result-value">{direction}</td>
</tr>
<tr>
    <td class="result-label">Lot Size</td>
    <td class="result-value">{lot}</td>
</tr>
<tr>
    <td class="result-label">Take Profit (1:3)</td>
    <td class="result-value">{tp}</td>
</tr>
</table>
""", unsafe_allow_html=True)

# ---------- COPYABLE VALUES ----------
st.markdown('<div class="copy-section"></div>', unsafe_allow_html=True)

st.text_input(
    "Copy Lot Size",
    value=str(lot),
    help="Tap and hold to copy"
)

st.text_input(
    "Copy Take Profit",
    value=str(tp),
    help="Tap and hold to copy"
)

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-note">Designed according to Biverway Trading System</div>',
    unsafe_allow_html=True
)
