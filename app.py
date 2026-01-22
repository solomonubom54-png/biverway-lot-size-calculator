import streamlit as st

st.set_page_config(
    page_title="Biverway | Lot Size Calculator",
    layout="centered"
)

# ----------------- HEADER -----------------
st.markdown(
    """
    <div style='background-color:#FFA500; color:black; padding:15px; text-align:center; font-size:28px; font-weight:bold; border-radius:10px;'>
        Biverway | Lot Size Calculator
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")  # space

# ----------------- INPUTS -----------------
st.markdown(
    "<div style='background-color:#f0f0f0; padding:10px; border-radius:5px; font-weight:bold;'>Inputs</div>",
    unsafe_allow_html=True
)
st.write("")  # small space

# Use a form so all inputs are in one block (keeps side-by-side clean)
with st.form("inputs_form"):
    # Symbol
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("Symbol")
    with col2:
        symbol = st.selectbox("", ["EURUSD", "GBPUSD", "USDCHF", "XAUUSD"], key="symbol_input")

    # Entry Price
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("Entry Price")
    with col2:
        entry = st.number_input("", format="%.5f", key="entry_input")

    # Stop Loss
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("Stop Loss")
    with col2:
        sl = st.number_input("", format="%.5f", key="sl_input")

    # Risk Amount
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("Risk Amount")
    with col2:
        risk = st.number_input("", min_value=1.0, format="%.2f", key="risk_input")

    submitted = st.form_submit_button("Calculate")

# ----------------- CALCULATIONS -----------------
if submitted:
    direction = "BUY" if entry > sl else "SELL"

    if symbol == "XAUUSD":
        point = round(abs(entry - sl) * 100, 1)
    else:
        point = abs(int(entry * 100000) - int(sl * 100000))

    if point == 0:
        st.warning("Entry price and Stop Loss are too close or identical. Adjust them.")
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

    # ----------------- OUTPUTS -----------------
    st.markdown(
        "<div style='background-color:#ADD8E6; padding:10px; border-radius:5px; font-weight:bold;'>Results</div>",
        unsafe_allow_html=True
    )
    st.write("")  # space

    # Output rows
    def output_row(label, value):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(label)
        with col2:
            st.markdown(value)

    output_row("Direction", direction)
    output_row("Price Diff (points)", point)
    output_row("Lot Size", lot_size)
    output_row("Take Profit (1:3)", tp)

# ----------------- FOOTER -----------------
st.write("")
st.markdown(
    "<i style='color:gray;'>Designed according to the Biverway Trading System. Risk-based lot sizing. Educational use only.</i>",
    unsafe_allow_html=True
)
