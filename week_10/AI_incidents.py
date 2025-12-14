import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from google import genai

from app.data.incidents import get_all_incidents
from app.data.db import connect_database

# -------------------------
# Gemini Client (SAFE)
# -------------------------
clients = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI Incident Analysis", layout="wide")
st.title("🤖 AI Cyber Incident Analysis")

# -------------------------
# Add New Incident
# -------------------------
st.subheader("Add New Incident")

with st.form("add_incident_form"):
    incident_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    category = st.text_input("Category")
    description = st.text_area("Description")
    reported_by = st.text_input("Reported By")

    submitted = st.form_submit_button("Add Incident")

    if submitted:
        if not incident_type or not description:
            st.error("Incident type and description are required.")
        else:
            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO cyber_incidents
                (incident_type, severity, category, status, description, reported_by)
                VALUES (?, ?, ?, 'Open', ?, ?)
            """, (incident_type, severity, category, description, reported_by))

            conn.commit()
            conn.close()

            st.success("Incident added successfully!")
            st.rerun()

# -------------------------
# Load Incidents
# -------------------------
incidents = get_all_incidents()
st.subheader("All Incidents")
st.dataframe(incidents, use_container_width=True)

if incidents.empty:
    st.info("No incidents available for analysis.")
    st.stop()

# -------------------------
# Select Incident
# -------------------------
incident_options = [
    f"{row['id']} | {row['incident_type']} ({row['severity']})"
    for _, row in incidents.iterrows()
]

selected_idx = st.selectbox(
    "Select an incident to analyse:",
    range(len(incidents)),
    format_func=lambda i: incident_options[i]
)

incident = incidents.iloc[selected_idx]

# -------------------------
# Incident Details
# -------------------------
st.subheader("Incident Details")
st.write(f"**Type:** {incident['incident_type']}")
st.write(f"**Severity:** {incident['severity']}")
st.write(f"**Category:** {incident['category']}")
st.write(f"**Status:** {incident['status']}")
st.write(f"**Description:** {incident['description']}")

# -------------------------
# AI Analysis
# -------------------------
if st.button("Analyse with AI", type="primary"):
    with st.spinner("AI analysing incident..."):
        prompt = f"""
        You are a cybersecurity expert.

        Analyse the following cyber incident:

        Type: {incident['incident_type']}
        Severity: {incident['severity']}
        Category: {incident['category']}
        Status: {incident['status']}
        Description: {incident['description']}

        Provide:
        1. Root cause analysis
        2. Immediate response actions
        3. Long-term prevention measures
        4. Risk assessment
        """

        try:
            response = clients.models.generate_content(
                model="gemini-pro",
                contents=prompt
            )
            st.subheader("🧠 AI Analysis Result")
            st.markdown(response.text)

        except Exception as e:
            st.error("AI analysis failed. Please try again later.")

