# Real-Time-Quant-Analysis-Dashboard
Real-Time Quantitative Analytics Dashboard
This project is a real-time quantitative analytics dashboard that streams live cryptocurrency market data from Binance and analyzes the relationship between two assets. It applies statistical techniques such as spread analysis, Z-score normalization, correlation tracking, and stationarity testing to study divergence and mean-reversion behavior through interactive visualizations.

# Features

- Live cryptocurrency price streaming using Binance WebSocket API
- Time-based resampling (1s, 1m, 5m) for clean time-series analysis
- Pair-based analysis using hedge ratio and spread calculation
- Z-score computation to detect statistical divergence
- Rolling correlation to monitor relationship stability
- Augmented Dickey-Fuller (ADF) test with visual stationarity diagnostics
- Real-time interactive charts and dashboards
- Z-score threshold alerts for abnormal movements
- Exportable analytics data in CSV format

# Tech Stack

- Python
- Streamlit (real-time dashboard)
- Plotly (interactive visualizations)
- Pandas & NumPy (data processing)
- Statsmodels (statistical testing)
- Binance WebSocket API (live market data)


