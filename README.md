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

# System Flow

<p align="center">
  <img src="assets/real%20time%20quant%20analysis%20dashboard.png" 
       alt="System Flow Diagram" 
       width="800"/>
</p>

<p align="center">
  <em>System flow illustrating real-time data movement from ingestion to analytics and dashboard visualization.</em>
</p>

# Tech Stack

- Python
- Streamlit (real-time dashboard)
- Plotly (interactive visualizations)
- Pandas & NumPy (data processing)
- Statsmodels (statistical testing)
- Binance WebSocket API (live market data)

# AI Usage

AI tools were used only as development assistance, primarily for code structuring, debugging support, documentation refinement, and architecture diagram generation. All analytical logic, statistical methods, and system design decisions were implemented and validated by the developer.
