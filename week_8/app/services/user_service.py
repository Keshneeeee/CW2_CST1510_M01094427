import sqlite3 #Library to interact with SQL database
import bcrypt #For secure password hashing
from pathlib import Path #For handling file paths and filesystem operations
from week_8.app.data.db import connect_database, DATA_DIR  # Function to establish a database connection


def register_user(username, password, role='user'): #Register a new user with hash password and role
   conn = connect_database() #Connecting to new database
   cursor = conn.cursor() #Creating a cursor object to update SQL commands
   #SQL commands to check if username already exist in the users table
   cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
   if cursor.fetchone(): #indicates username already exists if the record is found
       conn.close() #Close the transaction
       return False, f"Username '{username}' already exists." #Information message
   password_bytes = password.encode('utf-8') #Converts password strings to bytes
   salt = bcrypt.gensalt() #Generating salt for security
   hashed = bcrypt.hashpw(password_bytes, salt) #Hash the password with salt
   password_hash = hashed.decode('utf-8') #Decode hashed password to stare as string
   #Execute SQL query to insert new user to the user table with hashed password and role
   cursor.execute(
       "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
       (username, password_hash, role)
   )
   conn.commit() #Commit the SQL transaction
   conn.close() #Close the transaction
#Indicates successful registration of user and prints a confirmation message
   return True, f"User '{username}' registered successfully!" #

#Function to authenticate a user by verifying their password
def login_user(username, password):
    conn = connect_database() #Connect to database
    cursor = conn.cursor()
    #Execute SQL query to select username from user
    cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone() #Attempt to retrieve record from user
    conn.close() #Close the transaction

#Message if no user record was found
    if not user:
        return False, "Username not found."
    stored_hash = user[2] #Retrieve password hash from user record
    # Encode both password and stored hash into bytes as required by bcrypt
    password_bytes = password.encode('utf-8')
    hash_bytes = stored_hash.encode('utf-8')

#Use bcrypt.checkpw to compare input password and stored hash
    if bcrypt.checkpw(password_bytes, hash_bytes):
        return True, f"Welcome, {username}!" #Success message
    else:
        return False, "Invalid password." #failed message

#Function to to migrate users from a text file into the database
def migrate_users_from_file(conn, filepath = DATA_DIR/"users.txt"):
    file_path = Path(filepath) #Ensures filepath is an object
    if not file_path.exists(): #Checks if the file exist before proceeding
        print(f'File "{file_path}" does not exist.')
        print("No users to migrate")
        return False
    cursor = conn.cursor()
    migrated_count = 0 #tracks the number of migrated user

#Open file in read mode
    with open(filepath, 'r') as file:
        for line in file: #Read each line in the file
            line = line.strip()
            if not line: #Skip empty lines
                continue
            parts = line.strip().split(',') #Split lines into comma
            if len(parts) >= 2: #Ensure the line has at least a username and password
                username =  parts[0]
                password = parts[1]

                try: #Try to insert the user in the database
                    #'Insert or ignore' avoids duplicate entries
                    cursor.execute(
                        "Insert OR Ignore into users (username, password) VALUES (?, ?, ?)",
                        (username, password, 'users')
                    )
                    if cursor.rowcount > 0: #Checks if a row was actually inserted
                        migrated_count += 1
                except sqlite3.Error as e: #error message if insertion failed
                    print(f"Error migrating user {username}: {e}")

        conn.commit() #Commit the transaction
        print(f"Migrated {migrated_count} users from {filepath.name}")

        # Verify users were migrated
        conn = connect_database()
        cursor = conn.cursor()

        # Query all users
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall() #Fetch all user records

        print(" Users in database:")
        print(f"{'ID':<5} {'Username':<15} {'Role':<10}") #Print user records in formatted columns
        print("-" * 35)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

        print(f"\nTotal users: {len(users)}") #Print total number of users retrieved
        conn.close() #close transaction


    







