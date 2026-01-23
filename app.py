import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- STYLES (NO DARK LOGIC HERE) ----------------
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
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    border-radius:4px;
    margin-top:14px;
}

.result-header {
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    margin-top:14px;
    border-radius:4px;
}

.result-table {
    width:100%;
    border-collapse:collapse;
}

.result-table td {
    border:1px solid #ccc;
    padding:10px;
}

.result-label {
    background:#f5f5f5;
    font-weight:normal;
}

.result-value {
    background:#eef6ff;
    font-weight:bold;
    text-align:left;
}

.note {
    font-size:12px;
    text-align:center;
    margin-top:6px;
    opacity:0.7;
}

@media (max-width: 768px) {
    .sticky {
        position:fixed;
        bottom:0;
        left:0;
        right:0;
        padding:10px;
        background:var(--background-color);
        box-shadow:0 -2px 8px rgba(0,0,0,0.2);
        z-index:999;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])
    entry = st.number_input("Entry Price", format="%.5f")

with col2:
    sl = st.number_input("Stop Loss", format="%.5f")
    risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f")

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
<div class="sticky">
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
<div class="note">
Designed according to the Biverway Trading System.<br>
Risk-based lot sizing. Educational use only.
</div>
</div>
""", unsafe_allow_html=True)
