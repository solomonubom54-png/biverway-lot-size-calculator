import streamlit as st

# ----------------------------------
# Biverway Lot Size Calculator
# Version: v1.4+
# Sticky Results Test
# ----------------------------------

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "symbol" not in st.session_state:
    st.session_state.symbol = "EURUSD"
    st.session_state.entry = 0.0
    st.session_state.sl = 0.0
    st.session_state.risk = 0.0

# ---------- RESET FUNCTION ----------
def reset_all():
    st.session_state.entry = 0.0
    st.session_state.sl = 0.0
    st.session_state.risk = 0.0

# ---------- HIDE STREAMLIT UI ----------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- STYLES ----------
st.markdown("""
<style>

/* PAGE WIDTH */

.block-container{
    padding-top:1.2rem;
    padding-bottom:1rem;
    max-width:600px;
}

/* HEADER */

.header{
    background:#f5a623;
    padding:18px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:10px;
    margin-bottom:20px;
    color:#000;
}

/* SECTION TITLES */

.section{
    background:#d9edf7;
    padding:10px;
    font-weight:bold;
    border-radius:8px;
    margin-top:20px;
    margin-bottom:12px;
    color:#000;
}

/* STICKY RESULTS PANEL */

.results-panel{
    position:sticky;
    bottom:0;
    background:#ffffff;
    padding-top:10px;
}

/* RESULT TABLE */

.result-table{
    width:100%;
    border-collapse:collapse;
    margin-top:8px;
}

.result-table td{
    border:1px solid #dcdcdc;
    padding:12px;
    font-size:14px;
    color:#111;
}

.result-label{
    background:#f7f7f7;
    color:#111;
}

.result-value{
    background:#eef6ff;
    font-weight:bold;
    color:#111;
}

/* FOOTER */

.footer-note{
    margin-top:26px;
    margin-bottom:40px;
    font-size:12px;
    color:#666;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(
'<div class="header">Biverway | Lot Size Calculator</div>',
unsafe_allow_html=True
)

# ---------- INPUTS ----------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

symbol = st.selectbox(
    "Symbol",
    ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"],
    key="symbol",
    on_change=reset_all
)

price_format = "%.3f" if symbol == "XAUUSD" else "%.5f"

entry = st.number_input(
    "Entry Price",
    format=price_format,
    key="entry"
)

sl = st.number_input(
    "Stop Loss",
    format=price_format,
    key="sl"
)

risk = st.number_input(
    "Risk Amount",
    format="%.2f",
    key="risk"
)

st.button("Reset All", on_click=reset_all)

# ---------- VALIDATION ----------
inputs_ready = entry > 0 and sl > 0 and risk > 0 and entry != sl

# ---------- DEFAULT VALUES ----------
direction = "—"
lot = "0.00"
tp_display = format(0, ".3f" if symbol == "XAUUSD" else ".5f")

# ---------- CALCULATIONS ----------
if inputs_ready:

    direction = "BUY" if entry > sl else "SELL"

    if symbol == "XAUUSD":
        point = abs(entry - sl) * 100
    else:
        point = abs(int(entry * 100000) - int(sl * 100000))

    if symbol == "USDCHF":
        lot_raw = (risk * entry) / point
    else:
        lot_raw = risk / point

    lot_rounded = round(lot_raw, 2)
    lot = f"{lot_rounded:.2f}"

    if symbol == "XAUUSD":
        tp_dist = abs(entry - sl) * 3
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".3f")
    else:
        tp_dist = (point * 3) / 100000
        tp_val = entry + tp_dist if direction == "BUY" else entry - tp_dist
        tp_display = format(tp_val, ".5f")

# ---------- FORMAT DIRECTION ----------
if direction == "BUY":
    direction_display = "BUY ↑"
elif direction == "SELL":
    direction_display = "SELL ↓"
else:
    direction_display = "—"

# ---------- RESULTS ----------
st.markdown('<div class="results-panel">', unsafe_allow_html=True)

st.markdown('<div class="section">Results</div>', unsafe_allow_html=True)

rows = f"""
<tr>
<td class="result-label">Direction</td>
<td class="result-value">{direction_display}</td>
</tr>
<tr>
<td class="result-label">Lot Size</td>
<td class="result-value">{lot}</td>
</tr>
<tr>
<td class="result-label">Take Profit (1:3)</td>
<td class="result-value">{tp_display}</td>
</tr>
"""

st.markdown(f"""
<table class="result-table">
{rows}
</table>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
'<div class="footer-note">Designed according to Biverway Trading System · v1.4+</div>',
unsafe_allow_html=True
    )
