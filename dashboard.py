import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Test", page_icon="✅")

st.title("✅ Dashboard Test")
st.success("If you see this, it works!")

st.write(f"Current time: {datetime.now()}")
st.write(f"Python is working!")

if st.button("Click to Test"):
    st.balloons()
    st.success("✅ Button clicked successfully!")
