import streamlit as st
from config import settings

st.set_page_config(
    page_title="FinDash - Stock Market Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'SPY']

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {
        'AAPL': {'shares': 10, 'avg_price': 150.0},
        'MSFT': {'shares': 5, 'avg_price': 300.0}
    }

st.title("📈 FinDash Market Intelligence")
st.markdown("""
Welcome to **FinDash**, your professional stock market analytics dashboard.
Please select a module from the sidebar to begin.

### Modules:
- **Dashboard:** Real-time stock analysis, interactive candlestick charts, and technical indicators.
- **Portfolio:** Track your simulated holdings, profit/loss, and portfolio allocation.
""")

st.info("💡 Tip: Use the sidebar to navigate between the Dashboard and Portfolio views.")
