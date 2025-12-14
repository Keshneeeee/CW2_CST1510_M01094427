import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from google import genai

from app.data.it_tickets import get_all_it_tickets
from app.data.db import connect_database

# -------------------------
# Gemini Client
# -------------------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="AI IT Ticket Analysis", layout="wide")
st.title("🤖 AI IT Ticket Analysis")

# -------------------------
# Add New IT Ticket
# -------------------------
st.subheader("Add New IT Ticket")

with st.form("add_ticket_form"):
    ticket_id = st.text_input("Ticket ID")
    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    subject = st.text_input("Subject")
    description = st.text_area("Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    assigned_to = st.text_input("Assigned To")
    resolution_time = st.number_input(
        "Resolution Time (hours)", min_value=0.0, step=1.0
    )

    submitted = st.form_submit_button("Add Ticket")

    if submitted:
        if not ticket_id or not subject:
            st.error("Ticket ID and Subject are required.")
        else:
            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO it_tickets
                (ticket_id, priority, description, status, assigned_to, resolution_time_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ticket_id,
                priority,
                description,
                status,
                assigned_to,
                resolution_time
            ))

            conn.commit()
            conn.close()

            st.success("IT Ticket added successfully!")
            st.rerun()

# -------------------------
# Load Tickets
# -------------------------
tickets = get_all_it_tickets()

st.subheader("All IT Tickets")
st.dataframe(tickets, use_container_width=True)

if tickets.empty:
    st.info("No IT tickets available for analysis.")
    st.stop()

# -------------------------
# Select Ticket
# -------------------------
ticket_options = [
    f"{row['id']} | {row['ticket_id']} ({row['priority']})"
    for _, row in tickets.iterrows()
]

selected_idx = st.selectbox(
    "Select a ticket to analyse:",
    range(len(tickets)),
    format_func=lambda i: ticket_options[i]
)

ticket = tickets.iloc[selected_idx]

# -------------------------
# Ticket Details
# -------------------------
st.subheader("Ticket Details")
st.write(f"**Ticket ID:** {ticket['ticket_id']}")
st.write(f"**Priority:** {ticket['priority']}")
st.write(f"**Status:** {ticket['status']}")
st.write(f"**Assigned To:** {ticket['assigned_to']}")
st.write(f"**Description:** {ticket['description']}")
st.write(f"**Resolution Time (hrs):** {ticket['resolution_time_hours']}")

# -------------------------
# AI Analysis
# -------------------------
if st.button("Analyse Ticket with AI", type="primary"):
    with st.spinner("AI analysing ticket..."):
        prompt = f"""
        You are an IT service management expert.

        Analyse the following IT support ticket:

        Ticket ID: {ticket['ticket_id']}
        Priority: {ticket['priority']}
        Status: {ticket['status']}
        Assigned To: {ticket['assigned_to']}
        Description: {ticket['description']}
        Resolution Time (hours): {ticket['resolution_time_hours']}

        Provide:
        1. Likely root cause
        2. Recommended immediate actions
        3. Escalation necessity
        4. Suggestions to reduce resolution time
        """

        try:
            response = client.models.generate_content(
                model="gemini-pro",
                contents=prompt
            )

            st.subheader("🧠 AI Ticket Analysis")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"AI analysis failed: {e}")
