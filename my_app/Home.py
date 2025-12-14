import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from week_8.app.data.db import connect_database
from week_8.app.data.incidents import get_all_incidents
from week_8.app.data.it_tickets import get_all_it_tickets
from week_8.app.data.datasets import get_all_dataset
from week_8.app.data.users import get_all_users
from week_8.app.services.user_service import register_user, login_user
from week_8.app.data.schema import create_all_tables


def get_csv_stats(folder_path="datasets"):
    stats = []

    if not os.path.exists(folder_path):
        return pd.DataFrame()

    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                stats.append({
                    "File Name": file,
                    "Rows": df.shape[0],
                    "Columns": df.shape[1],
                    "File Size (KB)": round(os.path.getsize(file_path) / 1024, 2),
                })
            except:
                stats.append({
                    "File Name": file,
                    "Rows": "ERROR",
                    "Columns": "ERROR",
                    "File Size (KB)": "ERROR",
                })

    return pd.DataFrame(stats)

st.set_page_config(page_title="Home", layout="wide")

# ✅ Ensure all DB tables exist before anything runs
conn = connect_database()
create_all_tables(conn)
conn.close()

light_theme = """
<style>
body {
    background-color: #f6f7fb;
    color: #000000;
}
.dashboard-card {
    background: white;
    color: black;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.kpi-card {
    border-radius: 12px;
    padding: 25px;
}
</style>
"""

dark_theme = """
<style>
body {
    background-color: #0e1117;
    color: white !important;
}
.dashboard-card {
    background: #161a23;
    color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0px 2px 8px rgba(255,255,255,0.1);
}
.kpi-card {
    border-radius: 12px;
    padding: 25px;
}
</style>
"""
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

light_theme = """ ... """
dark_theme = """ ... """

st.set_page_config(page_title="Home", layout="wide")

if st.session_state["theme"] == "light":
    st.markdown(light_theme, unsafe_allow_html=True)
else:
    st.markdown(dark_theme, unsafe_allow_html=True)

def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

def logout():
    st.session_state["user"] = None
    st.session_state["role"] = None
    st.success("Logged out successfully!")

if st.session_state["user"] is None:

    st.title("Multi-Domain Intelligence Platform")
    st.write("Please login or register to continue.")
    st.write("Loading...")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            success, message = login_user(username, password)

            if success:
                st.session_state["user"] = username
                conn = connect_database()
                cur = conn.cursor()
                cur.execute("SELECT role FROM users WHERE username = ?", (username,))
                row = cur.fetchone()
                st.session_state["role"] = row[0] if row else "user"
                conn.close()

                st.success(f"Welcome User '{username}'! Logged in as '{st.session_state['role']}'")
                st.rerun()
            else:
                st.error("Login Failed. Invalid username or password.")

    with register_tab:
        st.subheader("Register New User")

        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")
        role = st.selectbox("Select Role", ["User", "Analyst", "Admin"])
        register_button = st.button("Register")

        if register_button:
            if not new_username or not new_password or not confirm_password:
                st.error("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match!")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                try:
                    success, message = register_user(new_username, new_password, role)
                    if success:
                        st.success(f"Registration Successful! User '{new_username}' created. Please log in.")
                    else:
                         st.error(message)
                except sqlite3.IntegrityError:
                    st.error(f"Username '{new_username}' already exists.")
                except Exception as e:
                    st.error(f"An unexpected error occurred during registration: {e}")

st.success(f"Logged in as '{st.session_state['user']}' (Role: {st.session_state['role']})")
st.button("Logout", on_click=logout)

theme_col1, theme_col2 = st.columns([3, 1])
with theme_col2:
    if st.button("Toggle Theme" if st.session_state["theme"] == "light" else "Toggle Theme"):
        toggle_theme()
        st.rerun()

st.title("Home Dashboard")

df_incidents = get_all_incidents()
df_tickets = get_all_it_tickets()
df_datasets = get_all_dataset()
all_users = get_all_users()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Incidents", len(df_incidents))
col2.metric("Total IT Tickets", len(df_tickets))
col3.metric("Total Datasets", len(df_datasets))
col4.metric("users", len(all_users))

st.write("---")

with st.sidebar:
    st.header("Navigation")

    if st.button("Dashboard"):
        st.switch_page("pages/Dashboard.py")

    if st.button("AI Cyber Incidents"):
        st.switch_page("week_10/AI_incidents.py")

    if st.button("AI IT Tickets"):
        st.switch_page("week_10/AI_tickets.py")

    if st.button("AI Datasets"):
        st.switch_page("week_10/AI_datasets.py")

st.write("---")
st.markdown("Visualization")

st.subheader("User Creation Trends")
users_df = get_all_users()
if not users_df.empty:
    fig, ax = plt.subplots()
    users_df['created_at'] = pd.to_datetime(users_df['created_at'])
    users_df.groupby(users_df['created_at'].dt.date).size().plot(kind='bar', ax=ax)
    ax.set_title("Users Created Over Time")
    st.pyplot(fig)

st.subheader("Incidents by Type Chart")
if not df_incidents.empty:
    fig_type = px.bar(
        df_incidents,
        x="category",
        title="Incidents by Category",
        labels={"category": "Incident Category"},
        color="category"
    )
    st.plotly_chart(fig_type, use_container_width=True)
else:
    st.info("No incident data available.")

st.subheader("IT Tickets by Priority Chart")
if not df_tickets.empty:
    fig_priority = px.bar(
        df_tickets,
        x="priority",
        title="Ticket Priority Distribution",
        labels={"priority": "Ticket Priority"},
        color="priority"
    )
    st.plotly_chart(fig_priority, use_container_width=True)
else:
    st.info("No ticket data available.")

st.subheader("Datasets Uploaded by User Chart")
if not df_datasets.empty:
    uploader_counts = df_datasets["uploaded_by"].value_counts()
    fig_ds, ax_ds = plt.subplots()
    ax_ds.bar(uploader_counts.index, uploader_counts.values)
    ax_ds.set_xlabel("Uploader")
    ax_ds.set_ylabel("Dataset Count")
    ax_ds.set_title("Datasets Uploaded by User")
    plt.xticks(rotation=45)
    st.pyplot(fig_ds)
else:
    st.info("No dataset metadata available.")

st.write("---")
st.header("CSV File Statistics")

def load_csv_files():
    data = {}
    csv_folder = "datasets"
    csv_map = {
        "incidents": ["incident", "incidents"],
        "tickets": ["ticket", "tickets"],
        "datasets": ["dataset", "datasets"],
        "users": ["user", "users"]
    }

    for csv_name in os.listdir(csv_folder):
        if csv_name.endswith(".csv"):
            lower = csv_name.lower()
            file_path = os.path.join(csv_folder, csv_name)
            df = pd.read_csv(file_path)

            for key, keywords in csv_map.items():
                if any(kw in lower for kw in keywords):
                    data[key] = df

    return data

csv_data = load_csv_files()

df_incidents = csv_data.get("incidents", pd.DataFrame())
df_tickets   = csv_data.get("tickets", pd.DataFrame())
df_datasets  = csv_data.get("datasets", pd.DataFrame())
users_df     = csv_data.get("users", pd.DataFrame())

st.write("---")

st.markdown("Navigation")

role = st.session_state["role"]

nav1, nav2, nav3, nav4 = st.columns(4)

if role in ["Analyst", "Admin"]:
    if nav1.button("Dashboard"):
        st.switch_page("Dashboard.py")

if role in ["Analyst", "Admin"]:
    if nav2.button("Cyber Incidents"):
        st.switch_page("Cyber_Incidents.py")

if role in ["User", "Admin"]:
    if nav3.button("IT Tickets"):
        st.switch_page("IT_Tickets.py")

if nav4.button("Datasets"):
    st.switch_page("Datasets.py")

st.write("---")

















