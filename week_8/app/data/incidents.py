import pandas as pd
from week_8.app.data.db import connect_database #Import custom database connection function
#Function to insert a new cyber incidents into the database
def insert_incident(timestamp, incident_type, severity, category, status, description, reported_by=None):
    conn = connect_database() #Connect to SQLite database
    cursor = conn.cursor() #Create a cursor object to execute SQL commands
    #Inserting new incident record to the cyber incident table
    cursor.execute("""
        INSERT INTO cyber_incidents
        (timestamp, incident_type, severity, category, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, incident_type, severity, category, status, description, reported_by))
    conn.commit() #Commit to save changes
    incident_id = cursor.lastrowid #Retrieve id of the new incident record
    conn.close() #Close the transaction
    return incident_id #Return the new incident id

#Function to retrieve all incidents
def get_all_incidents():
    conn = connect_database() #Connect to SQLite database
    #Read and load all result into a pandas dataframe in descending order
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df #Return the results

#Function to update icidents status
def update_incident_status(incident_id, new_status):
    conn = connect_database() #Connect to the SQLite database
    cursor = conn.cursor() #Create a cursor to execute SQL commands
    #Execute a SQL query to update the incident status and id
    cursor.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit() #Commit to save changes
    rows_affected = cursor.rowcount #Count the number of rows affected
    conn.close() #Close the transaction
    return rows_affected #Return the number of rows affected

#Function to delete incidents by their id
def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    #Execute an SQL query to delete incident id
    cursor.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    rows_affected = cursor.rowcount #Count the number of rows affected
    conn.close()
    return rows_affected #Return the number of rows affected









