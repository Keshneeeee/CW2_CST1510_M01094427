import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from google import genai

from app.data.datasets import get_all_dataset
from app.data.db import connect_database

# -------------------------
# Gemini Client
# -------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Dataset Analysis", layout="wide")
st.title("📊 AI Dataset Analysis")

# -------------------------
# Load Datasets
# -------------------------
datasets = get_all_dataset()

st.subheader("Available Datasets")
st.dataframe(datasets, use_container_width=True)

if datasets.empty:
    st.info("No datasets available for analysis.")
    st.stop()

# -------------------------
# Select Dataset
# -------------------------
dataset_options = [
    f"{row['id']} | {row['name']} ({row['domain']})"
    for _, row in datasets.iterrows()
]

selected_idx = st.selectbox(
    "Select a dataset to analyse:",
    range(len(datasets)),
    format_func=lambda i: dataset_options[i]
)

dataset = datasets.iloc[selected_idx]

st.subheader("Dataset Details")
st.write(f"**Name:** {dataset['name']}")
st.write(f"**Rows:** {dataset['rows']}")
st.write(f"**Columns:** {dataset['columns']}")
st.write(f"**Uploaded By:** {dataset['uploaded_by']}")
st.write(f"**Upload Date:** {dataset['upload_date']}")

if st.button("Analyse Dataset with AI", type="primary"):
    with st.spinner("AI analysing dataset..."):

        prompt = f"""
        You are a data analyst and cybersecurity intelligence expert.

        Analyse the following dataset metadata:

        Dataset Name: {dataset['name']}
        Number of Rows: {dataset['rows']}
        Number of Columns: {dataset['columns']}
        Uploaded By: {dataset['uploaded_by']}
        Upload Date: {dataset['upload_date']}

        Provide:
        1. What insights this dataset could be used for
        2. Potential analytical or security use cases
        3. Risks related to dataset size or sensitivity
        4. Recommendations for using this dataset effectively
        """

        try:
            response = client.models.generate_content(
                model="gemini-pro",
                contents=prompt
            )

            st.subheader("🧠 AI Dataset Analysis")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"AI analysis failed: {e}")
