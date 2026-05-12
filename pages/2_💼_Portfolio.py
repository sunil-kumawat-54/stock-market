import streamlit as st
import pandas as pd
import plotly.express as px
from services.market_data import get_live_price

st.set_page_config(page_title="Portfolio | FinDash", page_icon="💼", layout="wide")

st.title("💼 Portfolio Tracker")
st.write("Track your simulated holdings and performance.")

if 'portfolio' not in st.session_state or not st.session_state.portfolio:
    st.info("Your portfolio is empty. Add some holdings to get started!")
    st.stop()

portfolio = st.session_state.portfolio

# Calculate current values
total_value = 0
total_cost = 0
holdings_data = []

with st.spinner("Fetching live prices..."):
    for ticker, data in portfolio.items():
        shares = data['shares']
        avg_price = data['avg_price']
        cost_basis = shares * avg_price
        
        current_price = get_live_price(ticker)
        if current_price:
            current_value = shares * current_price
            unrealized_pl = current_value - cost_basis
            unrealized_pl_pct = (unrealized_pl / cost_basis) * 100
        else:
            current_price = avg_price
            current_value = cost_basis
            unrealized_pl = 0
            unrealized_pl_pct = 0
            
        total_value += current_value
        total_cost += cost_basis
        
        holdings_data.append({
            'Ticker': ticker,
            'Shares': shares,
            'Avg Cost': f"${avg_price:.2f}",
            'Current Price': f"${current_price:.2f}",
            'Total Cost': f"${cost_basis:.2f}",
            'Current Value': f"${current_value:.2f}",
            'Unrealized P/L': unrealized_pl,
            'P/L %': unrealized_pl_pct
        })

total_pl = total_value - total_cost
total_pl_pct = (total_pl / total_cost) * 100 if total_cost > 0 else 0

# Summary Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Portfolio Value", f"${total_value:,.2f}", f"${total_pl:,.2f} ({total_pl_pct:.2f}%)")
with col2:
    st.metric("Total Cost Basis", f"${total_cost:,.2f}")
with col3:
    st.metric("Total Return", f"${total_pl:,.2f}", f"{total_pl_pct:.2f}%")

st.markdown("---")

# Visualizations
st.subheader("Portfolio Allocation")
df_holdings = pd.DataFrame(holdings_data)
df_chart = df_holdings.copy()
df_chart['Current Value (Num)'] = df_chart['Current Value'].replace('[\$,]', '', regex=True).astype(float)

fig = px.pie(df_chart, values='Current Value (Num)', names='Ticker', hole=0.4, title="Allocation by Value", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Holdings Details")

# Format for display
display_df = df_holdings.copy()
display_df['Unrealized P/L'] = display_df['Unrealized P/L'].apply(lambda x: f"${x:,.2f}")
display_df['P/L %'] = display_df['P/L %'].apply(lambda x: f"{x:,.2f}%")

def color_surplus_deficit(val):
    color = 'green' if '-' not in str(val) and val != '$0.00' and val != '0.00%' else ('red' if '-' in str(val) else '')
    return f'color: {color}'

st.dataframe(
    display_df.style.map(color_surplus_deficit, subset=['Unrealized P/L', 'P/L %']),
    use_container_width=True
)

# Management
with st.expander("Manage Holdings"):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_t = st.text_input("Ticker").upper()
    with col2:
        new_s = st.number_input("Shares", min_value=0.0, step=1.0)
    with col3:
        new_p = st.number_input("Average Price", min_value=0.01)
        
    if st.button("Add/Update Holding"):
        if new_t:
            if new_s > 0:
                st.session_state.portfolio[new_t] = {'shares': new_s, 'avg_price': new_p}
                st.success(f"Updated {new_t}")
            else:
                if new_t in st.session_state.portfolio:
                    del st.session_state.portfolio[new_t]
                    st.success(f"Removed {new_t}")
            st.rerun()
