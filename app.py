import streamlit as st

st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ---------- HEADER ----------
st.markdown("""
<div style="
    background:#f5a623;
    padding:12px;
    font-size:24px;
    font-weight:bold;
    text-align:center;
    border-radius:6px;
">
Biverway | Lot Size Calculator
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- INPUTS TITLE ----------
st.markdown("""
<div style="
    background:#eeeeee;
    padding:6px;
    font-weight:bold;
    border-radius:4px;
">
Inputs
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- ROW HELPERS ----------
def input_row(label, widget):
    col1, col2 = st.columns([1.1, 2])
    with col1:
        st.markdown(f"<div style='padding-top:6px;'>{label}</div>", unsafe_allow_html=True)
    with col2:
        return widget

def output_row(label, value):
    col1, col2 = st.columns([1.1, 2])
    with col1:
        st.markdown(f"<div style='padding-top:6px;'>{label}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<div style='background:#eef6ff; padding:6px; border-radius:4px;'>{value}</div>",
            unsafe_allow_html=True
        )

# ---------- INPUT ROWS ----------
symbol = input_row(
    "Symbol",
    st.selectbox(
        "",
        ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"],
        key="symbol",
        label_visibility="collapsed"
    )
)

entry = input_row(
    "Entry Price",
    st.number_input(
        "",
        format="%.5f",
        key="entry_price",
        label_visibility="collapsed"
    )
)

sl = input_row(
    "Stop Loss",
    st.number_input(
        "",
        format="%.5f",
        key="stop_loss",
        label_visibility="collapsed"
    )
)

risk = input_row(
    "Risk Amount",
    st.number_input(
        "",
        min_value=1.0,
        format="%.2f",
        key="risk_amount",
        label_visibility="collapsed"
    )
)

st.write("")

# ---------- CALCULATIONS ----------
direction = "BUY" if entry > sl else "SELL"

if symbol == "XAUUSD":
    point = round(abs(entry - sl) * 100, 1)
else:
    point = abs(int(entry * 100000) - int(sl * 100000))

if point == 0:
    lot_size = 0
    tp = entry
else:
    if symbol == "USDCHF":
        lot_size = (risk * entry) / point
    else:
        lot_size = risk / point

    lot_size = round(lot_size, 2)

    if symbol == "XAUUSD":
        tp_distance = abs(entry - sl) * 3
    else:
        tp_distance = (point * 3) / 100000

    tp = entry + tp_distance if direction == "BUY" else entry - tp_distance
    tp = round(tp, 5)

# ---------- RESULTS TITLE ----------
st.markdown("""
<div style="
    background:#d9edf7;
    padding:6px;
    font-weight:bold;
    border-radius:4px;
">
Results
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- OUTPUT ROWS ----------
output_row("Direction", direction)
output_row("Price Diff (points)", point)
output_row("Lot Size", lot_size)
output_row("Take Profit (1:3)", tp)

# ---------- FOOTER ----------
st.write("")
st.markdown("""
<div style="color:gray; font-size:12px;">
Designed according to the Biverway Trading System.<br>
Risk-based lot sizing. Educational use only.
</div>
""", unsafe_allow_html=True)
