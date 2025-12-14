import pandas as pd
from week_8.app.data.db import connect_database
def get_user_by_username(username): #Retrieve user record from the database by the username
    conn = connect_database() #Establish a connection to the database
    cursor = conn.cursor() #Create a cursor object using the connection
    #Execute a parameterized query to avoid SQL injection
    cursor.execute(
        "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone() #Fetch the first matching user record
    conn.close() #Close the database connection
    return user
#Function to insert a new user in the database
def insert_user(username, password_hash, role='user'):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "Insert into users (username, password_hash, role) values (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit() #Commit the transaction to save changes to the database
    conn.close() #Close the database connection

def get_all_users():
    conn = connect_database()
    df = pd.read_sql_query(
        "select * from users",
        conn
    )
    conn.close()
    return df

#Function to update user's role
def update_user_role(username, role):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (role, username)
    )
    conn.commit()
    conn.close()
#Function to delete user role
def delete_user_role(username, role):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE username = ?",
    )
    conn.commit()
    conn.close()


