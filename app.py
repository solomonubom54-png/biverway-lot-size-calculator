import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>

/* GLOBAL */
body {
    background: #ffffff;
}

/* HEADER */
.header {
    background:#f5a623;
    padding:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
}

/* SECTION TITLES */
.section {
    background:#d9edf7;
    padding:6px;
    font-weight:bold;
    border-radius:4px;
    margin-top:12px;
}

/* TABLE */
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
    background:#f5f5f5;
    width:45%;
}

.value {
    background:#eef6ff;
    font-weight:bold;
    text-align:left;
}

/* STICKY RESULTS */
.sticky {
    position: sticky;
    bottom: 0;
    background: #ffffff;
    z-index: 100;
    padding-bottom: 10px;
}

/* ANIMATION */
.flash {
    animation: flash 0.6s;
}

@keyframes flash {
    0% { background-color: #fff3cd; }
    100% { background-color: #eef6ff; }
}

/* NOTE */
.note {
    font-size:12px;
    color:#666;
    margin-top:8px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"], key="symbol")
    entry = st.number_input("Entry Price", format="%.5f", key="entry")

with c2:
    sl = st.number_input("Stop Loss", format="%.5f", key="sl")
    risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f", key="risk")

# ---------------- CALCULATIONS ----------------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = abs(entry - sl) * 100
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
    tp = entry + tp_distance if direction == "BUY" else entry - tp_distance
    tp = round(tp, 5)

# ---------------- RESULTS ----------------
st.markdown('<div class="section sticky">Results</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="sticky">
<table class="table">
<tr>
    <td class="label">Direction</td>
    <td class="value flash">{direction}</td>
</tr>
<tr>
    <td class="label">Lot Size</td>
    <td class="value flash">{lot}</td>
</tr>
<tr>
    <td class="label">Take Profit (1:3)</td>
    <td class="value flash">{tp}</td>
</tr>
</table>

<div class="note">
Designed according to the Biverway Trading System.<br>
Risk-based lot sizing. Educational use only.
</div>
</div>
""", unsafe_allow_html=True)
