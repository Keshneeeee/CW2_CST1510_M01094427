import pandas as pd #Importing pandas function
from week_8.app.data.db import connect_database #importing database connection function
#funtion to insert new it tickets to the database
def insert_it_tickets(ticket_id, priority, subject, description, status, assigned_to=None, created_at=None, resolution_time_hours=None):
    conn = connect_database() #Connecting to the database
    cursor = conn.cursor() #Creating a new cursor object to execute SQL commands
    #Insert new records to the new it tickets table
    cursor.execute(""" 
    Insert into it_tickets
    (ticket_id, priority, subject, description, status, assigned_to, created_at, resolution_time_hours)
    values (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, subject, description, status, assigned_to, created_at, resolution_time_hours))
    conn.commit() #Commit to the transaction to save changes
    ticket_id = cursor.lastrowid #Retrive the id of the new it tickets id
    conn.close() #Close the data connection
    return ticket_id #Return the new ticket id

#Function to retrieve the ticket id
def get_all_it_tickets():
   conn = connect_database() #Connecting to the database
   #Execute a SQL query to fetch all it_tickets ordered by most first recents
   df = pd.read_sql_query(
       "select * from it_tickets order by id DESC",
       conn
   )
   conn.close() #close the database connection
   return df #Return results as a panne

#Function to update tickets status
def update_tickets_status(ticket_id, new_status):
    conn = connect_database() #Connecting to the database
    cursor = conn.cursor() #Creating new cursor object to update SQL commands
    #Updating new records to the new it tickets table
    cursor.execute("UPDATE it_tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
    conn.commit() #Commit the transaction to save changes
    rows_affected = cursor.rowcount #Get the number of rows affected by the update query
    conn.close() #Close the database connection
    return rows_affected #Return the number of updated rows

#Function to delete it_ticket status
def delete_tickets_status(ticket_id):
    conn = connect_database() #connecting new database
    cursor = conn.cursor() #Create new cursor object to execute SQL commands
    #SQL query to delete a record from it_tickets table
    #Use of parameterised input to prevent SQL injection
    cursor.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit() #Commit the transaction to apply deletion
    rows_affected = cursor.rowcount #Count the number of rows affected by deletion
    conn.close() #Close the database connection
    return rows_affected #Return the number of rows after deletion

