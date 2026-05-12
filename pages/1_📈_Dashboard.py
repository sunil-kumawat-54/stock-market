import streamlit as st
from services.market_data import get_stock_data, get_stock_info, get_live_price
from components.charts import render_candlestick_chart
from components.metrics import render_key_metrics

st.set_page_config(page_title="Dashboard | FinDash", page_icon="📈", layout="wide")

st.title("📈 Market Dashboard")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    
    # Watchlist management
    st.subheader("Watchlist")
    new_ticker = st.text_input("Add Ticker (e.g. TSLA)").upper()
    if st.button("Add") and new_ticker:
        if new_ticker not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_ticker)
            st.success(f"Added {new_ticker}")
            st.rerun()

    selected_ticker = st.selectbox("Select Ticker to Analyze", st.session_state.watchlist)
    
    if st.button("Remove Selected Ticker"):
        if selected_ticker in st.session_state.watchlist and len(st.session_state.watchlist) > 1:
            st.session_state.watchlist.remove(selected_ticker)
            st.rerun()
            
    st.markdown("---")
    st.subheader("Chart Settings")
    period = st.selectbox("Time Period", ['1mo', '3mo', '6mo', '1y', '2y', '5y'], index=3)
    interval = st.selectbox("Interval", ['1d', '1wk', '1mo'], index=0)
    
    show_sma = st.checkbox("Show SMA (20, 50)", value=True)
    show_macd = st.checkbox("Show MACD", value=True)

# Main Content
if selected_ticker:
    st.header(f"Analysis for {selected_ticker}")
    
    with st.spinner(f"Fetching data for {selected_ticker}..."):
        info = get_stock_info(selected_ticker)
        df = get_stock_data(selected_ticker, period=period, interval=interval)
        live_price = get_live_price(selected_ticker)
    
    # Header metrics
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(
            label="Current Price",
            value=f"${live_price:.2f}" if live_price else "N/A",
            delta=f"{(info.get('regularMarketChangePercent', 0)):.2f}%" if info else "0%"
        )
    with col2:
        st.subheader(info.get('longName', selected_ticker) if info else selected_ticker)
        st.caption(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')}")
    
    st.markdown("---")
    
    # Chart
    st.subheader("Price Action")
    render_candlestick_chart(df, selected_ticker, show_sma=show_sma, show_macd=show_macd)
    
    st.markdown("---")
    
    # Metrics
    st.subheader("Key Statistics")
    render_key_metrics(info)
    
    # Company Summary
    with st.expander("Company Description"):
        st.write(info.get('longBusinessSummary', 'No description available.'))
