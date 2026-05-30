import streamlit as st
from datetime import datetime
import sys
import os

print("=" * 50)
print("🚀 DASHBOARD STARTING...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")
print("=" * 50)

st.set_page_config(page_title="Trading Dashboard", page_icon="📈", layout="wide")

st.title("📈 Trading Dashboard - DEBUG MODE")
st.success("✅ If you see this, the dashboard is working!")

st.write("**Debug Info:**")
st.write(f"- Current time: {datetime.now()}")
st.write(f"- Python version: {sys.version}")
st.write(f"- Working directory: {os.getcwd()}")

st.divider()

st.header("🎯 Test Section")
st.write("If you can see this, the dashboard is fully functional!")

if st.button("Click Me to Test"):
    st.balloons()
    st.success("✅ Button works! Dashboard is responsive!")
