# FinDash - Professional Stock Market Dashboard

A modern, responsive, and robust Streamlit-based stock market dashboard designed for financial analytics, portfolio tracking, and interactive data visualization.

## Features
- **Real-time & Historical Data:** Powered by `yfinance` to fetch accurate market data without API key limits.
- **Interactive Candlestick Charts:** Advanced plotting with `plotly` and technical indicators (SMA, MACD) via `pandas-ta`.
- **Portfolio Tracker:** Simulate holdings, calculate unrealized P/L, and visualize asset allocation.
- **Key Metrics Dashboard:** Deep dive into company financials (P/E, Market Cap, Dividend Yield, etc.).
- **Modular Architecture:** Production-ready folder structure (`components`, `services`, `pages`) for scalability.

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip

### 1. Clone & Environment Setup
Navigate to the project root and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables (Optional)
If you wish to use secondary APIs (Alpha Vantage, Finnhub), copy the `.env.example` file to `.env` and add your keys.
```bash
cp .env.example .env
```

### 4. Run the Application
```bash
streamlit run app.py
```

## Architecture Overview
- **`app.py`:** Main entry point and state initialization.
- **`pages/`:** Contains the Streamlit multipage views (Dashboard, Portfolio).
- **`components/`:** Reusable UI elements (Charts, Metrics Grid).
- **`services/`:** API abstraction layer (`market_data.py`).
- **`config/`:** Application settings and environment variable management.

## Testing & Validation
- **API Limits:** The application primarily uses `yfinance` which has generous implicit limits, but caching (`@st.cache_data`) is implemented extensively to minimize redundant calls and improve performance.
- **UI Responsiveness:** Test on various window sizes; Streamlit's column layout handles mobile viewports gracefully by stacking elements.
