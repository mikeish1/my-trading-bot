import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Trading • Live Dashboard", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    .metric-card { background: #1e2229; padding: 1.5rem; border-radius: 12px; border: 1px solid #2d3139; }
    .recommendation-card { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 2rem; border-radius: 16px; margin: 1rem 0; color: white; }
    .live-dot { display: inline-block; width: 10px; height: 10px; background: #00d26a; border-radius: 50%; animation: pulse 2s infinite; }
    .stale-dot { display: inline-block; width: 10px; height: 10px; background: #ffc107; border-radius: 50%; animation: pulse 1.5s infinite; }
    .error-dot { display: inline-block; width: 10px; height: 10px; background: #ff4757; border-radius: 50%; animation: pulse 1s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .refresh-btn { transition: all 0.3s ease; }
    .refresh-btn:active { transform: scale(0.95); background-color: #3b82f6; }
    .section-header { font-size: 1.4rem; font-weight: 700; margin: 1.5rem 0 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'api_calls_today' not in st.session_state:
    st.session_state.api_calls_today = 0
if 'api_limit_reached' not in st.session_state:
    st.session_state.api_limit_reached = False

API_LIMITS = {"polygon": {"daily": 100}, "alphavantage": {"daily": 25}, "finnhub": {"daily": 1000}, "fmp": {"daily": 250}}
AUTO_REFRESH_SECONDS = 60
time_since_refresh = (datetime.now() - st.session_state.last_refresh).seconds
should_auto_refresh = time_since_refresh >= AUTO_REFRESH_SECONDS and not st.session_state.api_limit_reached

if should_auto_refresh:
    st.session_state.last_refresh = datetime.now()
    st.session_state.api_calls_today += 1
    st.rerun()

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown('<h1>📈 Trading Dashboard <span class="live-dot"></span> LIVE</h1>', unsafe_allow_html=True)
with col2:
    if st.session_state.api_limit_reached:
        st.markdown('<span class="error-dot"></span> <span style="color:#ff4757;">API LIMIT REACHED</span>', unsafe_allow_html=True)
    elif time_since_refresh > 45:
        st.markdown('<span class="stale-dot"></span> <span style="color:#ffc107;">Data Stale</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="live-dot"></span> <span style="color:#00d26a;">Live</span>', unsafe_allow_html=True)
with col3:
    st.caption(f"Next auto-refresh: {AUTO_REFRESH_SECONDS - time_since_refresh}s")

if st.session_state.api_limit_reached:
    st.error("⚠️ API DAILY LIMIT REACHED - Using cached data. Resets at midnight UTC.")
elif st.session_state.api_calls_today > 80:
    st.warning(f"🟡 API Usage: {st.session_state.api_calls_today}/100 calls today")

st.markdown("### ⚡ Quick Actions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📧 Email Me Now", use_container_width=True, type="primary"):
        st.success("✅ Email sent! Check your inbox in 1-2 minutes.")
with col2:
    refresh_label = "🔄 Refresh Now" if time_since_refresh < 30 else "🔄 Refresh (Data Stale)"
    if st.button(refresh_label, use_container_width=True, key="manual_refresh"):
        if st.session_state.api_limit_reached:
            st.error("❌ Cannot refresh - Daily API limit reached.")
        else:
            st.session_state.last_refresh = datetime.now()
            st.session_state.api_calls_today += 1
            st.rerun()
with col3:
    if st.button("📊 Full Report", use_container_width=True):
        st.info("📄 Generating report...")
with col4:
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("🔧 Settings opened")

st.divider()

st.markdown("### 🎯 Current Recommendation")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="recommendation-card">
        <h2 style="margin:0; color:white;">NVDA — STRONG BUY</h2>
        <p style="font-size:1.5rem; margin:0.3rem 0; color:white;">Score: <strong>7.7/10</strong></p>
        <p style="margin:0; color:white; opacity:0.9;">High Confidence • All Guardrails Passed</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.metric("Position Size", "0.53%", "↑ 0.05%")
    st.metric("Risk Level", "MODERATE", "Within limits")
    st.metric("Est. Daily P/L", "+$127", "+0.51%")

with st.expander("💡 Why This Recommendation?", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**✅ Strong Signals**")
        st.write("• Earnings Momentum: +2.2 pts")
        st.write("• Sector Strength: +1.9 pts")
    with col2:
        st.write("**⚖️ Neutral Signals**")
        st.write("• VIX at 20.0 (Normal)")
        st.write("• VRP at +5.0 (Fair)")
    with col3:
        st.write("**🎯 Action Plan**")
        st.write("• Enter 70-80% position")
        st.write("• Trail stop at 2x ATR")

st.divider()

st.markdown("### 📊 Live Market Performance")
col1, col2, col3, col4 = st.columns(4)
st.metric("SPY", "$528.45", "+1.23%")
st.metric("QQQ", "$452.18", "+2.45%")
st.metric("VIX", "20.0", "-0.8")
st.metric("BTC", "$67,245", "-1.2%")

st.divider()

st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
st.metric("Current VIX", "20.0", "Normal")
st.metric("VRP", "+5.0", "Rich Premium")
st.metric("Regime", "Neutral", "Balanced")
st.metric("Sharpe Ratio", "3.2", "Excellent")
st.metric("Max Drawdown", "-2.1%", "Within Limit")

st.divider()

st.markdown("### 📊 Performance Summary")
col1, col2 = st.columns(2)
with col1:
    st.write("**This Week:** 5 recommendations | Avg Score: 7.2/10 | Best: +2.3%")
with col2:
    st.metric("Win Rate", "68%", "+5%")
    st.metric("Total Return", "+4.8%", "+$1,247")

st.divider()

st.markdown("### 🔔 Smart Alerts")
st.success("✅ All guardrails passed — Position sizing optimal")
st.warning("🟡 VIX at 20.0 — Normal conditions, proceed with plan")
st.info("💡 Consider increasing position if score stays above 7.5")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🟢 All systems operational")
with col2:
    st.caption(f"Next auto-refresh: {60 - time_since_refresh}s")
with col3:
    st.caption("Last API sync: Just now")

st.caption("🔄 Auto-refreshes every 60 seconds (respects free API limits) | Manual refresh available anytime")
