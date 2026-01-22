import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------------- STATE ----------------
if "dark" not in st.session_state:
    st.session_state.dark = False

# ---------------- THEME TOGGLE ----------------
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
    background:{"#2a2a2a" if st.session_state.dark else "#eeeeee"};
    padding:8px;
    font-weight:bold;
    border-radius:4px;
    margin-top:14px;
}}

.label {{
    font-weight:normal;
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
}}

.result-value {{
    background:{"#121212" if st.session_state.dark else "#ffffff"};
    font-weight:bold;
    text-align:right;
    animation: glow 0.4s ease-in-out;
}}

@keyframes glow {{
    from {{ background:#fff3cd; }}
    to {{ background:{"#121212" if st.session_state.dark else "#ffffff"}; }}
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

col1, col2 = st.columns([1,1])

with col1:
    symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"], key="symbol")
    entry = st.number_input("Entry Price", format="%.5f", key="entry")

with col2:
    sl = st.number_input("Stop Loss", format="%.5f", key="sl")
    risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f", key="risk")

# ---------------- AUTO-FOCUS JS ----------------
st.markdown("""
<script>
const inputs = window.parent.document.querySelectorAll('input');
inputs.forEach((el, idx) => {
  el.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && inputs[idx+1]) {
      inputs[idx+1].focus();
    }
  });
});
</script>
""", unsafe_allow_html=True)

# ---------------- CALCULATIONS ----------------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    price_diff = round(abs(entry - sl), 2)
    point = price_diff * 100
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
<td class="result-label">Price Diff</td>
<td class="result-value">{point}</td>
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
