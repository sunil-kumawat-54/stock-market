import yfinance as yf
import pandas as pd
import streamlit as st
import time

@st.cache_data(ttl=300) # Cache for 5 minutes
def get_stock_data(ticker_symbol: str, period: str = '1y', interval: str = '1d'):
    """Fetch historical stock data using yfinance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period, interval=interval)
        if df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"Error fetching data for {ticker_symbol}: {e}")
        return None

@st.cache_data(ttl=300)
def get_stock_info(ticker_symbol: str):
    """Fetch key company metrics and info."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        return info
    except Exception as e:
        st.error(f"Error fetching info for {ticker_symbol}: {e}")
        return {}

def get_live_price(ticker_symbol: str):
    """Fetch near-real-time price (delayed up to 15m usually)."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period='1d', interval='1m')
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except Exception as e:
        return None
