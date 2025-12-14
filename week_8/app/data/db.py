#Define the path from SQLite to database file
#Data is the folder and the intelligence platform.db is the database file
import sqlite3 #sqlite database engine
import pandas as pd #For handling tabular data
import bcrypt #For secure password hashing
from pathlib import Path #for clean cross-platform filesystem paths

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"

# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

#Function to connect to database
def connect_database(db_path=DB_PATH):
    #Connect to SQL database
    return sqlite3.connect(str(db_path))

print("Using DB:", DB_PATH)
print(" Imports successful!") #Prints confirmation message
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")





