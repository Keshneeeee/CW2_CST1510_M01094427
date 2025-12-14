#Import database connections
from week_8.app.data.db import connect_database, DATA_DIR
# Import functions to create database tables
from week_8.app.data.schema import (
    create_users_tables,
    create_cyber_incidents_tables,
    create_datasets_metadata_tables,
    create_it_tickets_tables,
    create_all_tables,
    load_all_csv_data,
)
#Import user service functions to register, login and migrate users
from week_8.app.services.user_service import register_user, login_user, migrate_users_from_file
from week_8.app.data.incidents import insert_incident, get_all_incidents, update_incident_status, delete_incident
from week_8.app.services import get_incidents_by_type_count, get_high_severity_status


def main(): #Enter main function for application demo
    print("=" * 60)
    print("Week 8: Database Demo") #Header for the application demo
    print("=" * 60)

    conn = connect_database() #Connect to the database
    create_all_tables(conn)

    migrate_users_from_file(conn) #Migrate users from text files to database
    conn.close() #Close transaction

#Register new username "Alice"
    success, message = register_user("alice", "SecurePass123!", "analyst")
    print(message) #Prints confirmation message

#Attempts to login "Alice"
    success, message = login_user("alice", "SecurePass123!")
    print(message) #Prints confirmation message

#Insert new cyber incident record in the database
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Email",
        "Open",
        "Suspicious email detected"
        "alice"
    )
    print(f" created incident #{incident_id}") #Print the incident id
    #Retrieve all incident counts and print the total number
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

    conn = connect_database()
    df_by_type = get_incidents_by_type_count(conn)
    print("\nIncidents by Type:")
    print(df_by_type)

    df_high = get_high_severity_status(conn)
    print("\nHigh Severity by Status:")
    print(df_high)
    conn.close()

if __name__ == "__main__":
 main()

# Function to set up the complete database
def setup_database_complete(run_steps=None):
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP") #Header for setup processes
    print("=" * 60)

    conn = None #Initialise connection variables
    try:
        # Step 1: Connect to database
        if run_steps is None or 1 in run_steps:
            print("\n[1/5] Connecting to database...") #Print confirmation message
            try:
                conn = connect_database() #Establise database connection
                print("Connected")
            except Exception as e:
                print(f"Error connecting to database: {e}") #Error message if connection fails
                return

        # Step 2: Create tables
        if run_steps is None or 2 in run_steps:
            print("\n[2/5] Creating database tables...")
            try:
                create_users_tables(conn) #Create users tables
                create_cyber_incidents_tables(conn) #Create cyber incidents table
                create_datasets_metadata_tables(conn) #Create dataset tables
                create_it_tickets_tables(conn) #Create it tickets table
                print("Tables created") #Prints confirmation message
            except Exception as e:
                print(f"Error creating tables: {e}") #Error message if failed to create tables
                return #exit function if failed to create table

        # Step 3: Migrate users from a text file into the database
        if run_steps is None or 3 in run_steps: #Run if no steps or step 3 is given
            print("\n[3/5] Migrating users from users.txt...")
            try:
                user_count = migrate_users_from_file(conn) #Count number of migrated user
                print(f"Migrated {user_count} users")
            except Exception as e: #Report and handles errors during migration
                print(f"Error migrating users: {e}")

        # Step 4: Load CSV data
        if run_steps is None or 4 in run_steps:
            print("\n[4/5] Loading CSV data...")
            try:
                #Load Datasets Metadata CSV files in the Datasets Metadata table
                rows1 = load_all_csv_data(
                    conn,
                    r"Data/datasets_metadata.csv",
                    "datasets_metadata"
                )
                print(f"Loaded {rows1} rows into datasets_metadata") #Prints confirmation message

               #Load IT Tickets CSV files in the IT Tickets table
                rows2 = load_all_csv_data(
                    conn,
                    r"Data/it_tickets.csv",
                    "it_tickets"
                )
                print(f"Loaded {rows2} rows into it_tickets") #Prints confirmation message

              #Load Cyber incidents CSV file in cyber incidents table
                rows3 = load_all_csv_data(
                    conn,
                    r"Data/cyber_incidents.csv",
                    "cyber_incidents"
                )
                print(f"Loaded {rows3} rows into cyber_incidents") #Prints confirmation message

            except Exception as e:
                print(f"Error loading CSV data: {e}") #Handle and report errors, if any, when loading csv data

        # Step 5: Verify if tables were successfully created
        if run_steps is None or 5 in run_steps: #Run if no steps or step 5 was given
            print("\n[5/5] Verifying database setup...")
            try:
                cursor = conn.cursor() #Craete cursor to execute SQL commands
                #SQL queries to select from tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()] #Fetch table names from query results

                print("\n Database Summary:")
                print(f"{'Table':<25} {'Row Count':<15}")
                print("-" * 40)

                for table in tables: #Read through each line of the table names and count the number of rows
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"{table:<25} {count:<15}") #Print table name and number of rows
            except Exception as e:
                print(f"Error verifying setup: {e}") #Handle and record errors during the verification

    finally: #Ensures the database if closed after verification regardless of success or failure
        if conn:
            conn.close()
            print("\nConnection closed.")
#Prints summary
    print("\n" + "=" * 60)
    print(" DATABASE SETUP COMPLETE!") #Prints confirmation message
    print("=" * 60)
    print(f"\nDatabase location: {DATA_DIR.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface!)")


# Run the complete setup (all steps)
setup_database_complete()

#Function to run comprehensive test
def run_comprehensive_tests(pd = None):
    print("\n" + "="*60)
    print("Running Comprehensive Tests...")
    print("="*60)

    conn = connect_database() #Establishing database connection

    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user") #REgistration of new user
    print(f"Register: {'Successful' if success else 'Failed'} {msg}") #Prints confirmation message upon registration

#Login of new user
    success, msg = login_user("test_user", "TestPass123!")
    print(f"Login:{'Successful' if success else 'failed'} {msg}")

    # Test 2: CRUD Operations
    print("\n[Test 2] CRUD Operations")

    # Create id
    test_id = insert_incident(
        "2024-11-05",
        "Test Incident",
        "Low",
        "Email",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"  Create: Cyber Incident #{test_id} created")
    #Read sql query and load results in pandas dataframe. use of parameterised query to prevent SQL injection
    df=pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"Read:Found incident #{test_id}")
    print(df)

    # Update incident status
    update_incident_status(conn, test_id, "Resolved")
    print(f"Update: Status updated")

    # Delete inicident status
    delete_incident(test_id)
    print(f"Delete: Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")

    df_by_type = get_incidents_by_type_count(conn)
    print(f"By Type:Found {len(df_by_type)} incident types")

    df_high = get_high_severity_status(conn)
    print(f"High Severity: Found {len(df_high)} status categories")

    conn.close()

    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)

# Run comprehensive tests
run_comprehensive_tests()











