"""
=========================================================
Saad Python Project
dashboard.py
Version : 2.2
=========================================================
"""

import streamlit as st
import pandas as pd


class Dashboard:

    def show_metrics(self, responses):
        total = len(responses)
        success = sum(r["status"] == "success" for r in responses)
        failed = total - success
        avg = round(
            sum(r.get("time", 0) for r in responses) / total, 2
        ) if total else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Models", total)
        c2.metric("Success", success)
        c3.metric("Failed", failed)
        c4.metric("Avg Time (s)", avg)

    def show_table(self, responses):
        # Clean the dataframe - remove model_id column if present
        df = pd.DataFrame(responses)
        if "model_id" in df.columns:
            df = df.drop(columns=["model_id"])
        st.subheader("Model Responses")
        st.dataframe(df, use_container_width=True)

    def show_best(self, best, judge_name="Gemini 1.5 Flash"):
        st.subheader("🏆 Best Response")
        st.caption(f"Selected by: **{judge_name}** 🤖")
        st.markdown(f"**Model:** {best.get('model','N/A')}")
        st.write(best.get("response", ""))

    def render(self, responses, judge):
        self.show_metrics(responses)
        st.divider()
        self.show_table(responses)
        st.divider()
        # Use judge to select best
        best = judge.select_best(responses)
        self.show_best(best)


if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard Demo", layout="wide")

    sample = [
        {
            "model": "Groq Llama 3.1",
            "status": "success",
            "response": "Sample response from Groq.",
            "time": 1.12,
        },
        {
            "model": "Mistral Small",
            "status": "success",
            "response": "Longer sample response from Mistral.",
            "time": 1.48,
        },
        {
            "model": "OpenRouter Pro",
            "status": "failed",
            "response": "API Error",
            "time": 0.72,
        },
    ]

    from judge import Judge
    dashboard = Dashboard()
    judge = Judge()
    dashboard.render(sample, judge)