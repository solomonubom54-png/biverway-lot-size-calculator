import streamlit as st

st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
.header {
    background:#f5a623;
    padding:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
    margin-bottom:10px;
}

.section {
    background:#eeeeee;
    padding:6px;
    font-weight:bold;
    border-radius:4px;
    margin-top:12px;
}

.table {
    width:100%;
    border-collapse:collapse;
    margin-top:6px;
}

.table td {
    border:1px solid #ccc;
    padding:8px;
    font-size:14px;
}

.label {
    background:#f5f5f5;
    font-weight:bold;
    width:45%;
}

.value {
    background:#ffffff;
}

.result-header {
    background:#d9edf7;
    padding:6px;
    font-weight:bold;
    margin-top:12px;
    border-radius:4px;
}

.footer {
    margin-top:12px;
    font-size:12px;
    color:gray;
    font-style:italic;
    text-align:left;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

symbol = st.selectbox(
    "Symbol",
    ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"],
    label_visibility="collapsed"
)

entry = st.number_input(
    "Entry",
    format="%.5f",
    label_visibility="collapsed"
)

sl = st.number_input(
    "SL",
    format="%.5f",
    label_visibility="collapsed"
)

risk = st.number_input(
    "Risk",
    min_value=1.0,
    format="%.2f",
    label_visibility="collapsed"
)

st.markdown(f"""
<table class="table">
<tr>
    <td class="label">Symbol</td>
    <td class="value">{symbol}</td>
</tr>
<tr>
    <td class="label">Entry Price</td>
    <td class="value">{entry}</td>
</tr>
<tr>
    <td class="label">Stop Loss</td>
    <td class="value">{sl}</td>
</tr>
<tr>
    <td class="label">Risk Amount</td>
    <td class="value">{risk}</td>
</tr>
</table>
""", unsafe_allow_html=True)

# ---------------- CALCULATIONS ----------------
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

# ---------------- RESULTS ----------------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<table class="table">
<tr>
    <td class="label">Direction</td>
    <td class="value">{direction}</td>
</tr>
<tr>
    <td class="label">Price Diff</td>
    <td class="value">{point}</td>
</tr>
<tr>
    <td class="label">Lot Size</td>
    <td class="value">{lot}</td>
</tr>
<tr>
    <td class="label">Take Profit (1:3)</td>
    <td class="value">{tp}</td>
</tr>
</table>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">Designed according to the Biverway Trading System. Risk-based lot sizing. Educational use only.</div>',
    unsafe_allow_html=True
)
