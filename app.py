"""
app.py
------
Streamlit frontend for FreelanceOS.
Run locally with:  streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

from main import FreelanceInput, run_freelance_crew

load_dotenv()  # loads .env when running locally

st.set_page_config(page_title="FreelanceOS", page_icon="🤖", layout="wide")


def get_api_key() -> str:
    """Look for the key in Streamlit secrets (cloud), then environment (.env)."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass  # no secrets file locally, which is fine
    return os.getenv("GEMINI_API_KEY", "")


# ---------- Sidebar: settings ----------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", value=get_api_key(), type="password",
                            help="Get a free key at aistudio.google.com/apikey. On the cloud, use Secrets instead.")
      model = st.selectbox("Model", ["gemini-3.5-flash-lite", "gemini-3.5-flash"], index=0)
    st.caption("Free tier has rate limits; if you see a 429 error, wait a minute and retry.")

# ---------- Header ----------
st.title("🤖 FreelanceOS: The Agentic Copilot")
st.write("Paste a job post and let 4 AI agents scout it, pitch it, plan it and price it.")

# ---------- Input form ----------
with st.form("job_form"):
    job_description = st.text_area("📋 Job posting", height=200,
                                   placeholder="Paste the full job description here...")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your name", value="Alex")
        skills = st.text_input("Your skills", placeholder="Python, React, copywriting")
        experience = st.text_input("Experience", placeholder="3 years freelancing")
    with col2:
        rate = st.number_input("Hourly rate (USD)", min_value=1.0, value=50.0, step=5.0)
        availability = st.text_input("Availability", value="20 hours per week")
    submitted = st.form_submit_button("🚀 Run FreelanceOS", use_container_width=True)

# ---------- Run the crew ----------
if submitted:
    if not api_key:
        st.error("Please add your Gemini API key in the sidebar.")
    else:
        try:
            data = FreelanceInput(
                job_description=job_description, freelancer_name=name, skills=skills or "Not specified",
                experience=experience or "Not specified", hourly_rate=rate, availability=availability,
            )
        except ValidationError:
            st.error("Please paste a job description (at least 20 characters).")
        else:
            try:
                with st.spinner("🧠 Agents are working... this can take 1-3 minutes."):
                    st.session_state["results"] = run_freelance_crew(data, api_key, model)
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ---------- Display results ----------
if "results" in st.session_state:
    r = st.session_state["results"]
    st.success("✅ Done! Review each agent's output below.")
    tabs = st.tabs(["🔍 Lead Scout", "✍️ Proposal", "📅 Project Plan", "💰 Finance"])
    for tab, key in zip(tabs, ["lead_analysis", "proposal", "project_plan", "finance"]):
        with tab:
            st.markdown(r[key])

    # One-click download of everything as a markdown file
    full_report = (
        f"# FreelanceOS Report\n\n## Lead Analysis\n{r['lead_analysis']}\n\n"
        f"## Proposal\n{r['proposal']}\n\n## Project Plan\n{r['project_plan']}\n\n"
        f"## Finance\n{r['finance']}\n"
    )
    st.download_button("⬇️ Download full report", full_report, "freelanceos_report.md", "text/markdown")
