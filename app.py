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

.table {
    width:100%;
    border-collapse:collapse;
}

.table td {
    border:1px solid #ccc;
    padding:10px;
    font-size:14px;
}

.label {
    background:#f7f7f7;
    width:50%;
}

.value {
    background:#eef6ff;
    font-weight:bold;
}

.result-header {
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    border-radius:6px;
    margin-top:16px;
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

# Symbol
symbol = st.selectbox(
    "Symbol",
    ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"],
    label_visibility="collapsed"
)

price_format = "%.3f" if symbol == "XAUUSD" else "%.5f"

entry = st.number_input(
    "Entry Price",
    format=price_format,
    label_visibility="collapsed"
)

sl = st.number_input(
    "Stop Loss",
    format=price_format,
    label_visibility="collapsed"
)

risk = st.number_input(
    "Risk Amount",
    min_value=0.0,
    format="%.2f",
    label_visibility="collapsed"
)

# INPUT TABLE DISPLAY
st.markdown(f"""
<table class="table">
<tr>
    <td class="label">Symbol</td>
    <td class="value">{symbol}</td>
</tr>
<tr>
    <td class="label">Entry Price</td>
    <td class="value">{format(entry, ".3f" if symbol=="XAUUSD" else ".5f")}</td>
</tr>
<tr>
    <td class="label">Stop Loss</td>
    <td class="value">{format(sl, ".3f" if symbol=="XAUUSD" else ".5f")}</td>
</tr>
<tr>
    <td class="label">Risk Amount</td>
    <td class="value">{format(risk, ".2f")}</td>
</tr>
</table>
""", unsafe_allow_html=True)

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = abs(entry - sl) * 100
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

if point == 0 or risk == 0:
    lot = "0.00"
    tp_display = format(entry, ".3f" if symbol == "XAUUSD" else ".5f")
else:
    if symbol == "USDCHF":
        lot = f"{(risk * entry) / point:.2f}"
    else:
        lot = f"{risk / point:.2f}"

    if symbol == "XAUUSD":
        tp_val = entry + (abs(entry - sl) * 3) if direction == "BUY" else entry - (abs(entry - sl) * 3)
        tp_display = format(tp_val, ".3f")
    else:
        tp_val = entry + ((point * 3) / 100000) if direction == "BUY" else entry - ((point * 3) / 100000)
        tp_display = format(tp_val, ".5f")

# ---------- RESULTS ----------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<table class="table">
<tr>
    <td class="label">Direction</td>
    <td class="value">{direction}</td>
</tr>
<tr>
    <td class="label">Lot Size</td>
    <td class="value">{lot}</td>
</tr>
<tr>
    <td class="label">Take Profit (1:3)</td>
    <td class="value">{tp_display}</td>
</tr>
</table>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-note">Designed according to Biverway Trading System</div>',
    unsafe_allow_html=True
)
