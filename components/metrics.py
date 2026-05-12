import streamlit as st

def render_key_metrics(info: dict):
    """Render key financial metrics in a visually appealing grid."""
    if not info:
        st.warning("No metrics data available.")
        return

    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Market Cap", format_large_number(info.get('marketCap')))
        st.metric("Volume", format_large_number(info.get('volume')))
    with m2:
        st.metric("P/E Ratio", round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else "N/A")
        st.metric("Forward P/E", round(info.get('forwardPE', 0), 2) if info.get('forwardPE') else "N/A")
    with m3:
        div_yield = info.get('dividendYield', 0)
        st.metric("Dividend Yield", f"{div_yield * 100:.2f}%" if div_yield else "N/A")
        st.metric("Beta", round(info.get('beta', 0), 2) if info.get('beta') else "N/A")
    with m4:
        st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}" if info.get('fiftyTwoWeekHigh') else "N/A")
        st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 0):.2f}" if info.get('fiftyTwoWeekLow') else "N/A")

def format_large_number(num):
    if not num:
        return "N/A"
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    else:
        return f"${num:,.2f}"
