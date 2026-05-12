import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def render_candlestick_chart(df: pd.DataFrame, ticker: str, show_sma=True, show_macd=True):
    """Render interactive candlestick chart with Plotly."""
    if df is None or df.empty:
        st.warning("No data available for chart.")
        return
        
    # Calculate indicators
    if show_sma:
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
    
    if show_macd:
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD_12_26_9'] = exp1 - exp2
        df['MACDs_12_26_9'] = df['MACD_12_26_9'].ewm(span=9, adjust=False).mean()
        df['MACDh_12_26_9'] = df['MACD_12_26_9'] - df['MACDs_12_26_9']

    rows = 2 if show_macd else 1
    row_heights = [0.7, 0.3] if show_macd else [1.0]
    
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, row_heights=row_heights)

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], 
                                 low=df['Low'], close=df['Close'], name='Price'), 
                  row=1, col=1)

    if show_sma:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='cyan', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='orange', width=1)), row=1, col=1)

    if show_macd and 'MACD_12_26_9' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_12_26_9'], name='MACD', line=dict(color='cyan', width=1)), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACDs_12_26_9'], name='Signal', line=dict(color='orange', width=1)), row=2, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df['MACDh_12_26_9'], name='Histogram'), row=2, col=1)

    fig.update_layout(
        title=f"{ticker} Price Analysis",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark", # Looks good in dark mode
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
