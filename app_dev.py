import streamlit as st

# ----------------------------------
# Biverway Lot Size Calculator
# Version: v1.4-dev
# Development Version
# ----------------------------------

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator (Dev)",
    layout="centered"
)

# ---------- MOBILE VIEWPORT ----------
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
""", unsafe_allow_html=True)

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

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    max-width:600px;
}

.header{
    background:#f5a623;
    padding:16px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:8px;
    margin-bottom:18px;
    color:#000;
}

/* TERMINAL STYLE PANELS */

.panel{
    background:#ffffff;
    border:1px solid #dcdcdc;
    border-radius:10px;
    padding:16px;
    margin-bottom:18px;
    box-shadow:0 2px 6px rgba(0,0,0,0.06);
}

.panel-title{
    font-weight:bold;
    font-size:15px;
    margin-bottom:12px;
    color:#333;
}

/* RESULT TABLE */

.result-table{
    width:100%;
    border-collapse:collapse;
}

.result-table td{
    border:1px solid #e2e2e2;
    padding:12px;
    font-size:14px;
}

.result-label{
    background:#f7f7f7;
}

.result-value{
    background:#eef6ff;
    font-weight:bold;
}

.footer-note{
    margin-top:20px;
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

# ---------- INPUT PANEL ----------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Inputs</div>', unsafe_allow_html=True)

symbol = st.selectbox(
    "Symbol",
    ["EURUSD","GBPUSD","USDCHF","XAUUSD"],
    key="symbol",
    on_change=reset_all
)

price_format = "%.3f" if symbol=="XAUUSD" else "%.5f"

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

st.markdown('</div>', unsafe_allow_html=True)

# ---------- VALIDATION ----------
inputs_ready = entry>0 and sl>0 and risk>0 and entry!=sl

# ---------- DEFAULT VALUES ----------
direction="—"
lot="0.00"
actual_risk="0.00"
tp_display=format(0,".3f" if symbol=="XAUUSD" else ".5f")

# ---------- CALCULATIONS ----------
if inputs_ready:

    direction="BUY" if entry>sl else "SELL"

    if symbol=="XAUUSD":
        point=abs(entry-sl)*100
    else:
        point=abs(int(entry*100000)-int(sl*100000))

    if symbol=="USDCHF":
        lot_raw=(risk*entry)/point
    else:
        lot_raw=risk/point

    lot_rounded=round(lot_raw,2)
    lot=f"{lot_rounded:.2f}"

    if symbol=="USDCHF":
        actual_risk_val=lot_rounded*point/entry
    else:
        actual_risk_val=lot_rounded*point

    actual_risk=f"{actual_risk_val:.2f}"

    if symbol=="XAUUSD":
        tp_dist=abs(entry-sl)*3
        tp_val=entry+tp_dist if direction=="BUY" else entry-tp_dist
        tp_display=format(tp_val,".3f")
    else:
        tp_dist=(point*3)/100000
        tp_val=entry+tp_dist if direction=="BUY" else entry-tp_dist
        tp_display=format(tp_val,".5f")

# ---------- RESULTS PANEL ----------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Results</div>', unsafe_allow_html=True)

rows=f"""
<tr>
<td class="result-label">Direction</td>
<td class="result-value">{direction}</td>
</tr>
"""

if inputs_ready:
    rows+=f"""
<tr>
<td class="result-label">Actual Risk</td>
<td class="result-value">{actual_risk}</td>
</tr>
"""

rows+=f"""
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
'<div class="footer-note">Designed according to Biverway Trading System · v1.4-dev</div>',
unsafe_allow_html=True
    )
