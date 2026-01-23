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

.result-row {
    background:#eef6ff;
    padding:8px;
    border-radius:4px;
    margin-bottom:6px;
}

.result-label {
    font-weight:normal;
}

.footer-note {
    margin-top:18px;
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

symbol = st.selectbox("Symbol", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"])
entry = st.number_input("Entry Price", format="%.5f")
sl = st.number_input("Stop Loss", format="%.5f")
risk = st.number_input("Risk Amount", min_value=1.0, format="%.2f")

# ---------- CALCULATIONS ----------
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
    tp = round(entry + tp_distance if direction == "BUY" else entry - tp_distance, 5)

# ---------- RESULTS ----------
st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

# Direction (no copy)
c1, c2 = st.columns([1, 2])
with c1:
    st.markdown("**Direction**")
with c2:
    st.markdown(f"**{direction}**")

# Lot Size (copyable)
c1, c2, c3 = st.columns([1, 1.5, 1])
with c1:
    st.markdown("Lot Size")
with c2:
    st.markdown(f"**{lot}**")
with c3:
    st.code(lot)

# Take Profit (copyable)
c1, c2, c3 = st.columns([1, 1.5, 1])
with c1:
    st.markdown("Take Profit (1:3)")
with c2:
    st.markdown(f"**{tp}**")
with c3:
    st.code(tp)

# ---------- FOOTER ----------
st.markdown(
    '<div class="footer-note">Designed according to Biverway Trading System</div>',
    unsafe_allow_html=True
                    )
