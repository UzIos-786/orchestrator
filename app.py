"""
=========================================================
Saad Python Project
Main Application
Version : 2.2
=========================================================
"""

import asyncio
import streamlit as st

from config import (
    PROJECT_NAME,
    VERSION,
    APP_TITLE,
    PAGE_ICON,
    LAYOUT,
    SIDEBAR_STATE,
    AVAILABLE_MODELS,
)

from api_manager import APIManager
from judge import Judge
from dashboard import Dashboard

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)

st.title(APP_TITLE)
st.caption(f"{PROJECT_NAME} | Version {VERSION}")

st.sidebar.title("⚙ Settings")

selected_model = st.sidebar.selectbox(
    "Display Model", AVAILABLE_MODELS
)

temperature = st.sidebar.slider(
    "Temperature", 0.0, 1.0, 0.3, 0.1
)

max_tokens = st.sidebar.slider(
    "Max Tokens", 100, 4000, 1000, 100
)

st.divider()

prompt = st.text_area(
    "Enter your prompt",
    height=220
)

if st.button("🚀 Run All Models", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    with st.spinner("Querying AI models and judging responses..."):

        manager = APIManager()
        responses = asyncio.run(
            manager.ask_all_models(prompt)
        )

        # Use Gemini as judge
        judge = Judge()
        best = asyncio.run(judge.select_best_async(responses))
        
        dashboard = Dashboard()
        
        # Show metrics
        dashboard.show_metrics(responses)
        st.divider()
        
        # Show table
        dashboard.show_table(responses)
        st.divider()
        
        # Show best with judge info
        st.subheader("🏆 Best Response")
        st.caption(f"Selected by: **Gemini 1.5 Flash** 🤖")
        st.markdown(f"**Model:** {best.get('model','N/A')}")
        st.write(best.get("response", ""))

    st.divider()

    st.subheader("Raw Responses")

    for item in responses:
        with st.expander(item["model"], expanded=False):
            st.write(f"Status : {item['status']}")
            st.write(f"Time   : {item['time']} sec")
            st.write(item["response"])

st.divider()
st.caption("© 2026 UZ Python Project")
