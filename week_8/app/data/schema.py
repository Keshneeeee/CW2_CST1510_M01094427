import pandas as pd
from pathlib import Path

#Function to create users tables
def create_users_tables(conn):
    cursor = conn.cursor() #Create cursor object to create an SQL commands
    #Execute and SQL query to create users table.
    #The 'IF NOT EXISTS' ensures that we don't recreate the table if it already exists
    #Each user has a unique id
    #Username and password may not be unique
    #Hashed password should never be stored in a plain texts
    #User role defaults to normal user
    #Timestamps are auto added
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit() #Commit to save changes
    print("Users table created successfully") #Prints success message

#Function to create cyber incidents message
def create_cyber_incidents_tables(conn):
    cursor = conn.cursor() #create a cursor object to execute SQL query
    #Execute SQL query to create cyber incident table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            incident_type TEXT,
            timestamp TEXT,
            severity TEXT,
            category TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit() #Save the changes
    print("Cyber incidents table created successfully") #Confirmation message

#Function to create datasets metadata table
def create_datasets_metadata_tables(conn):
    cursor = conn.cursor()
    #SQL query to create the datasets metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id TEXT,
            name TEXT NOT NULL,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            uploaded_date TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit() #Save changes
    print("Datasets metadata table created successfully") #Confirmation message

#Function to create it tickets table
def create_it_tickets_tables(conn):
    cursor = conn.cursor() #Create cursor object to execute SQL commands
    #Creates the it tickets table
    #Ensure not to create the table again if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,       
            priority TEXT,                       
            description TEXT,                     
            status TEXT,                         
            assigned_to TEXT,                     
            created_at TEXT,                      
            resolution_time_hours REAL            
        );
    """)
    conn.commit() #Save the changes
    print("IT tickets table created successfully") #Confirmation message

#Function to create all tables
def create_all_tables(conn):
    create_users_tables(conn) #Set up the users table to manage login info and roles
    create_cyber_incidents_tables(conn) #Create cyber incident table to manage security incidents
    create_datasets_metadata_tables(conn) #Create datasets metadata data to store data
    create_it_tickets_tables(conn) #create a table to manage it tickets

#Function to load data from a csv file into a database table
def load_all_csv_data(conn, csv_path, table_name):
    try:
        df = pd.read_csv(csv_path) #Reads the CSV file in a pandas dataframe
        df.to_sql(table_name, conn, if_exists='replace', index=False) #shifts data into an SQLite dataframe
        row_count = len(df) #Count the number of rows loaded
        print(f"Successfully loaded {row_count} rows into {table_name}") #Confirmation message
        return row_count #Return the number of rows counted
    except FileNotFoundError: #Error message if file path is not found
        print(f"CSV not found: {csv_path}")
        return None
    except Exception as e: #Error message in CSV file is not loaded
        print(f"Error loading CSV {csv_path} -> {e}")
        return None









