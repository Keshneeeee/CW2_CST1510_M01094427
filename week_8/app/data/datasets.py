import pandas as pd
from week_8.app.data.db import connect_database #Import custom database connection function
#Function to insert a new dataset into the database
def insert_datasets(dataset_id, name, rows, columns, uploaded_by, uploaded_date, reported_by=None):
    conn = connect_database() #Connecting to the database
    cursor = conn.cursor() #Creating new cursor object to update SQL commands
    #Inserting new records to the datasets metadata
    cursor.execute("""
    insert into datasets_metadata
    (dataset_id, name, rows, columns, uploaded_by, uploaded_date, reported_by)
    values (?, ?, ?, ?, ?, ?, ?)
    """, (dataset_id, name, rows, columns, uploaded_by, uploaded_date, reported_by))
    conn.commit() #commit to save changes
    dataset_id = cursor.lastrowid #Retrieve the ID of the new Dataset id
    conn.close() #Close the transaction
    return dataset_id #Return the new datasets id

#Function to retrieve the ticket id
def get_all_dataset():
    conn = connect_database()
    #Execute SQL query and read results into pandas dataframe in descending order
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY uploaded_date DESC",
        conn
    )
    conn.close()
    return df #Return result as panne

#Function to update datasets id
def update_datasets_uploaded_by(dataset_id, uploaded_by):
    conn = connect_database()
    cursor = conn.cursor()
    #Updating new records to the new datasets metadata table. use of parametarised query to prevent SQL injection
    cursor.execute("UPDATE datasets_metadata SET uploaded_by = ? WHERE id = ?", (uploaded_by, dataset_id))
    conn.commit()
    rows_affected = cursor.rowcount #Count the number of rows affected by the update query
    conn.close()
    return rows_affected #Return the number of rows affected by the update query

#function to delete datasets records
def delete_datasets_uploaded_by(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()
    #Execute SQL query to delete datasets id.
    cursor.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    rows_affected = cursor.rowcount #Count number of rows deleted
    conn.close() #Close the transaction
    return rows_affected #Return the number of rows affected

