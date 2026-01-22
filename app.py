import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- STATE ----------------
if "dark" not in st.session_state:
    st.session_state.dark = False

# ---------------- DARK MODE TOGGLE ----------------
st.toggle("🌙 Dark Mode", key="dark")

# ---------------- STYLES ----------------
st.markdown(f"""
<style>
body {{
    background: {"#121212" if st.session_state.dark else "#ffffff"};
}}

.header {{
    background:#f5a623;
    padding:12px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
    color:#000;
}}

.section {{
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    border-radius:4px;
    margin-top:14px;
}}

input, select {{
    font-size:16px !important;
}}

.result-header {{
    background:#d9edf7;
    padding:8px;
    font-weight:bold;
    margin-top:14px;
    border-radius:4px;
}}

.result-table {{
    width:100%;
    border-collapse:collapse;
}}

.result-table td {{
    border:1px solid {"#444" if st.session_state.dark else "#ccc"};
    padding:10px;
}}

.result-label {{
    background:{"#1f1f1f" if st.session_state.dark else "#f5f5f5"};
    font-weight:normal;
}}

.result-value {{
    background:#eef6ff;
    font-weight:bold;
    text-align:left;
    animation: glow 0.4s ease-in-out;
}}

@keyframes glow {{
    from {{ background:#fff3cd; }}
    to {{ background:#eef6ff; }}
}}

@media (max-width: 768px) {{
    .sticky {{
        position:fixed;
        bottom:0;
        left:0;
        right:0;
        padding:10px;
        background:{"#121212" if st.session_state.dark else "#ffffff"};
        box-shadow:0 -2px 8px rgba(0,0,0,0.2);
        z-index:999;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"], key="symbol")
    entry = st.number_input("Entry Price", format="%.5f", key="entry")

with col2:
    sl = st.number_input("Stop Loss", format="%.5f", key="sl")
    risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f", key="risk")

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
</div>
""", unsafe_allow_html=True)

# ---------------- FOOTNOTE ----------------
st.caption(
    "Designed according to the Biverway Trading System. "
    "Risk-based lot sizing. Educational use only."
)
