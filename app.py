import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ingestion import BinanceWebSocket
from storage import TickStore
from analytics import spread_and_zscore, rolling_correlation, adf_test
from alerts import check_zscore_alert

st.set_page_config(layout="wide")

# =====================
# CONFIG
# =====================
SYMBOLS = ["BTCUSDT", "ETHUSDT"]

# =====================
# SESSION INIT
# =====================
if "ws" not in st.session_state:
    st.session_state.ws = BinanceWebSocket(SYMBOLS)
    st.session_state.ws.start()

if "store" not in st.session_state:
    st.session_state.store = TickStore()

# =====================
# UI
# =====================
st.title("Real-Time Quant Analytics Dashboard")
st.caption(f"Ticks collected: {len(st.session_state.store.df)}")

col1, col2, col3 = st.columns(3)
sym1 = col1.selectbox("Symbol X", SYMBOLS, index=0)
sym2 = col2.selectbox("Symbol Y", [s for s in SYMBOLS if s != sym1], index=0)
tf = col3.selectbox("Timeframe", ["1s", "1m", "5m"], index=1)

window = st.slider("Rolling Window", 10, 100, 30)
z_thresh = st.slider("Z-Score Alert Threshold", 1.0, 3.0, 2.0)

# =====================
# INGEST DATA
# =====================
ticks = list(st.session_state.ws.buffer)
st.session_state.ws.buffer.clear()

if ticks:
    st.session_state.store.update(ticks)

# =====================
# RESAMPLE
# =====================
df_x = st.session_state.store.resample(sym1, tf)
df_y = st.session_state.store.resample(sym2, tf)

if df_x.empty or df_y.empty:
    st.info("Streaming live data from Binance. Waiting for bars...")
    st.stop()

df = pd.concat([df_x["price"], df_y["price"]], axis=1)
df.columns = ["x", "y"]
df = df.dropna()

# =====================
# MIN DATA GUARD
# =====================
MIN_POINTS = max(window + 5, 50)

if len(df) < MIN_POINTS:
    st.warning(f"Collecting data... ({len(df)}/{MIN_POINTS})")

    # Plot 1 — price only
    st.subheader("Price Comparison")
    st.line_chart(df)
    st.stop()

# =====================
# ANALYTICS
# =====================
beta, spread, z = spread_and_zscore(df["x"], df["y"], window)
corr = rolling_correlation(df["x"], df["y"], window)

# =====================
# PLOT 1 — PRICE
# =====================
st.subheader("Price Comparison")
st.caption(
    "Displays the resampled price movement of both assets over time for relative trend comparison."
)
st.line_chart(df)

# =====================
# PLOT 2 — SPREAD + Z
# =====================
st.subheader("Spread & Z-Score")
st.caption(
    "Shows the hedge-ratio adjusted spread and its standardized Z-score to identify divergence and mean-reversion signals."
)

fig_spread = go.Figure()
fig_spread.add_trace(go.Scatter(y=spread, name="Spread"))
fig_spread.add_trace(go.Scatter(y=z, name="Z-Score"))
st.plotly_chart(fig_spread, use_container_width=True)

# =====================
# ALERT
# =====================
alert = check_zscore_alert(z.iloc[-1], z_thresh)
if alert:
    st.error(alert)

# =====================
# PLOT 3 — ADF DIAGNOSTIC
# =====================
st.subheader("Stationarity Diagnostics (ADF)")
st.caption(
    "Evaluates whether the spread is statistically stationary using the Augmented Dickey-Fuller test and visual diagnostics."
)


clean_spread = spread.dropna()

if len(clean_spread) >= 50:
    rm = clean_spread.rolling(window).mean()

    # Spread + rolling mean
    st.markdown("Spread with Rolling Mean")
    st.caption("Visual check for mean-reverting behavior by observing spread oscillation around its rolling mean.")

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=clean_spread.index, y=clean_spread, name="Spread"))
    fig1.add_trace(go.Scatter(x=rm.index, y=rm, name="Rolling Mean", line=dict(dash="dash")))
    fig1.update_layout(title="Spread with Rolling Mean")
    st.plotly_chart(fig1, use_container_width=True)

    # ADF statistic vs critical values
    st.markdown("ADF Statistic vs Critical Values")
    st.caption("Compares the ADF test statistic against critical thresholds to formally assess stationarity.")

    res = adf_test(clean_spread)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=list(res["Critical Values"].keys()),
        y=list(res["Critical Values"].values()),
        name="Critical Values"
    ))
    fig2.add_hline(
        y=res["ADF Statistic"],
        line_dash="dash",
        line_color="red",
        annotation_text=f"ADF = {res['ADF Statistic']:.3f}"
    )
    fig2.update_layout(title="ADF Statistic vs Critical Values")
    st.plotly_chart(fig2, use_container_width=True)

    if res["p-value"] < 0.05:
        st.success("Spread is stationary (mean-reverting).")
    else:
        st.warning("Spread is non-stationary.")

else:
    st.info("ADF diagnostics will appear once sufficient data is available.")

# =====================
# EXPORT
# =====================
st.download_button(
    "Download CSV",
    df.assign(spread=spread, zscore=z).to_csv().encode(),
    "analytics.csv"
)


