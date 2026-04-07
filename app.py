import streamlit as st
import engine
import data_fetcher
import pandas as pd

# 1. Page Title and Icon
st.set_page_config(page_title="Pakistan Financial EWS", page_icon="🇵🇰")

st.title("🇵🇰 Financial Stability Early Warning System")
st.markdown("---")

# 2. The Sidebar (For the API Sync)
st.sidebar.header("Data Controls")
if st.sidebar.button("🔄 Sync Live World Bank Data"):
    with st.spinner("Fetching latest data..."):
        stats = data_fetcher.get_pakistan_stats()
        st.session_state['inf'] = stats['inflation']
        st.session_state['ir'] = stats['interest_rate']
        st.session_state['gdp'] = stats['gdp_growth']
        st.sidebar.success("Data Synced!")

# 3. Organizing the Input Fields
st.subheader("📊 Economic Indicators")
col1, col2 = st.columns(2)

with col1:
    # We use session_state so the API data stays in the box
    inf = st.number_input("Inflation % (API)", value=st.session_state.get('inf', 12.0))
    ir = st.number_input("Interest Rate (API)", value=st.session_state.get('ir', 10.0))
    db = st.number_input("Debt-to-GDP Proxy (API)", value=st.session_state.get('gdp', 2.5))

with col2:
    ex = st.number_input("Exchange Rate Risk (Manual)", min_value=0.0, max_value=100.0, value=30.0)
    fx = st.number_input("Forex Reserve Risk (Manual)", min_value=0.0, max_value=100.0, value=30.0)
    stk = st.number_input("Stock Volatility (Manual)", min_value=0.0, max_value=100.0, value=20.0)

# 4. The Calculation and Result
st.markdown("---")
if st.button("🚀 Assess Stability Risk", use_container_width=True):
    score, status, color = engine.calculate_stability(inf, ex, fx, ir, db, stk)
    
    # Show a big "Metric" card
    st.metric(label="Calculated Stability Score", value=score)
    
    if "Stable" in status:
        st.success(f"Result: {status}")
    elif "Moderate" in status:
        st.warning(f"Result: {status}")
    else:
        st.error(f"Result: {status}")

# 5. The Graph Section
st.markdown("---")
st.subheader("📈 10-Year Historical Inflation Trend")
if st.checkbox("Show Historical Chart"):
    years, values = data_fetcher.get_historical_inflation()
    chart_data = pd.DataFrame(values, index=years, columns=["Inflation %"])
    st.line_chart(chart_data)