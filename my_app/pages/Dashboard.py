import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from week_8.app.data.datasets import get_all_dataset
from week_8.app.data.incidents import get_all_incidents
from week_8.app.data.it_tickets import get_all_it_tickets
from week_8.app.data.users import get_all_users

st.set_page_config(page_title="Dashboard", layout="wide")

if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

if st.session_state["user"] is None:
    st.error("Error: You must be logged in to access this page.")
    if st.button("Back"):
        st.switch_page("Home.py")
    st.stop()

st.title("Dashboard")
st.success(f"Hello, {st.session_state['user']}! You are logged in.")

def dashboard_page():
    st.title("Dashboard Overview")

    theme = st.radio("Choose Theme:", ["Light", "Dark"], horizontal=True)
    plotly_theme = "seaborn" if theme == "Light" else "plotly_dark"
    mpl_style = "default" if theme == "Light" else "dark_background"
    plt.style.use(mpl_style)

    incidents_df = get_all_incidents()
    datasets_df = get_all_dataset()
    tickets_df = get_all_it_tickets()
    users_df = get_all_users()

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Incidents", len(incidents_df))
    col2.metric("Datasets", len(datasets_df))
    col3.metric("Tickets", len(tickets_df))
    col4.metric("Users", len(users_df))

    st.divider()

    st.subheader("Incident Analytics")
    if not incidents_df.empty:
        colA, colB = st.columns(2)
        with colA:
            fig1 = px.bar(
                incidents_df,
                x='severity',
                title="Incidents by Severity",
                text_auto=True,
                template=plotly_theme
            )
            st.plotly_chart(fig1, use_container_width=True)
        with colB:
            fig2 = px.pie(
                incidents_df,
                names='status',
                title="Incidents by Status",
                template=plotly_theme
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Datasets Analytics")
    datasets_df['uploaded_date'] = pd.to_datetime(datasets_df['uploaded_date'])
    fig = px.bar(
        datasets_df.groupby(datasets_df['uploaded_date'].dt.date).size().reset_index(name="count"),
        x="uploaded_date",
        y="count",
        title="Datasets Uploaded Over Time",
        text_auto=True,
        template=plotly_theme
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Ticket Priorities")
    if not tickets_df.empty:
        fig3 = px.pie(
            tickets_df,
            names='priority',
            title="Tickets by Priority",
            template=plotly_theme
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.subheader("User Creation Trends")
    if not users_df.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        users_df['created_at'] = pd.to_datetime(users_df['created_at'])
        users_df.groupby(users_df['created_at'].dt.date).size().plot(
            kind='bar', ax=ax, color="pink"
        )
        ax.set_title("Users Created Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Users")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    st.divider()

    st.subheader("CSV Files Statistics")

    def show_csv_stats(path, label):
        try:
            df = pd.read_csv(path)
            st.metric(f"{label}", f"{len(df)} rows")
        except FileNotFoundError:
            st.metric(f"{label}", "File not found")

    import sqlite3

    def show_db_stats(db_path, label, table_name):
        try:
            conn = sqlite3.connect(db_path)
            query = f"SELECT COUNT(*) FROM {table_name}"
            count = pd.read_sql_query(query, conn).iloc[0, 0]
            st.metric(label, f"{count} rows")
            conn.close()
        except Exception as e:
            st.error(f"{label} error: {e}")

    colX, colY, colZ, colA = st.columns(4)
    with colX:
        show_csv_stats('week_8/Data/cyber_incidents.csv', "Cyber Incidents CSV")
    with colY:
        show_csv_stats('week_8/Data/datasets_metadata.csv', "Datasets Metadata CSV")
    with colZ:
        show_csv_stats('week_8/Data/it_tickets.csv', "IT Tickets CSV")
    with colA:
        show_db_stats('week_8/Data/intelligence_platform.db', "Intelligence Platform DB", table_name="Intelligence Platform DB")

st.divider()
dashboard_page()

if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You are logged out.")
    st.switch_page("Home.py")