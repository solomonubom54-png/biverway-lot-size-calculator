import streamlit as st

st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ------------------ STATE ------------------
if "dark" not in st.session_state:
    st.session_state.dark = False

# ------------------ TOGGLE ------------------
st.toggle("🌙 Dark Mode", key="dark")

# ------------------ THEME ------------------
bg = "#0e1117" if st.session_state.dark else "#ffffff"
text = "#eaeaea" if st.session_state.dark else "#000000"
card = "#161b22" if st.session_state.dark else "#f7f9fc"
accent = "#4da3ff"
border = "#2a2f3a" if st.session_state.dark else "#d0d7de"

st.markdown(f"""
<style>
body {{
    background:{bg};
    color:{text};
}}

.header {{
    background:#f5a623;
    padding:14px;
    font-size:22px;
    font-weight:bold;
    text-align:center;
    border-radius:8px;
    color:#000;
}}

.section {{
    margin-top:14px;
    padding:8px;
    font-weight:bold;
}}

.card {{
    background:{card};
    border:1px solid {border};
    border-radius:10px;
    padding:12px;
}}

.label {{
    font-size:14px;
}}

.result-box {{
    position:sticky;
    bottom:0;
    background:{card};
    border:2px solid {accent};
    border-radius:12px;
    padding:12px;
    margin-top:14px;
    animation: pulse 0.4s ease-in-out;
}}

@keyframes pulse {{
    0% {{ box-shadow:0 0 0 {accent}; }}
    100% {{ box-shadow:0 0 12px {accent}; }}
}}

.result-row {{
    display:flex;
    justify-content:space-between;
    padding:6px 0;
}}

.result-value {{
    font-weight:bold;
    color:{accent};
}}

.note {{
    font-size:12px;
    opacity:0.7;
    margin-top:8px;
}}
</style>

<script>
document.addEventListener("DOMContentLoaded", function() {{
    let inputs = document.querySelectorAll("input");
    inputs.forEach((el, i) => {{
        el.addEventListener("keydown", e => {{
            if (e.key === "Enter" && inputs[i+1]) {{
                inputs[i+1].focus();
            }}
        }});
    }});
});
</script>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="header">Biverway | Lot Size Calculator</div>', unsafe_allow_html=True)

# ------------------ INPUTS ------------------
st.markdown('<div class="section">Inputs</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])
entry = st.number_input("Entry Price", format="%.5f", key="entry")
sl = st.number_input("Stop Loss", format="%.5f", key="sl")
risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f", key="risk")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ CALCULATION ------------------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    price_diff = round(abs(entry - sl) * 100, 1)
else:
    price_diff = abs(int(entry * 100000) - int(sl * 100000))

if price_diff == 0:
    lot = 0
    tp = entry
else:
    lot = round(risk / price_diff, 2)
    tp_distance = abs(entry - sl) * 3
    tp = round(entry + tp_distance if direction == "BUY" else entry - tp_distance, 5)

# ------------------ RESULTS ------------------
st.markdown('<div class="section">Results</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="result-box">
    <div class="result-row">
        <span>Direction</span>
        <span class="result-value">{direction}</span>
    </div>
    <div class="result-row">
        <span>Lot Size</span>
        <span class="result-value">{lot}</span>
    </div>
    <div class="result-row">
        <span>Take Profit (1:3)</span>
        <span class="result-value">{tp}</span>
    </div>
</div>

<div class="note">
Designed according to the Biverway Trading System. Risk-based lot sizing. Educational use only.
</div>
""", unsafe_allow_html=True)
