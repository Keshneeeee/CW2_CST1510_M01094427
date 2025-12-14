import bcrypt #Import the bcrypt library for password hashing
import os #Import the os library

USER_DATA_FILE = "Users.txt" #file path to store username and hashed passw2ord

#Function to define hashed password
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8') #Convert the password string to bytes
    salt = bcrypt.gensalt() #Genrating salt for security
    hashed_password = bcrypt.hashpw(password_bytes, salt) #Hash the password with salt
    return hashed_password.decode('utf-8')  #Return the password as string

#Function to verify password
def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8') #convert password strings to bytes
    hashed_password_bytes = hashed_password.encode('utf-8') #Convert hashed password string to bytes
    return bcrypt.checkpw(password_bytes, hashed_password_bytes) #return results

#Function to register user
def register_user(username, password):
    #Checks if username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.") #Print error message if username already exists
        return False
    hashed_password = hash_password(password) #If the user doesn't exist, hash the provided password
    #Add the new user to the file
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n") #write the new username and the hashed password in the new file
    print(f"User '{username}' registered successfully") #Print the success message
    return True

#Function to check if username already exists in user file
def user_exists(username):
    #Open user file in read mode
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                user, _ = line.strip().split(',', 1)
                if user == username:
                    return True #Return true if username matches
    except FileNotFoundError:  #Assume usernamme aren't registered yet if file doesn't exist
        return False
    return False

#Function to login username and password
def login_user(username, password):
    #Open user file in read mode
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f.readlines(): #Read through each line in the file
                user, hash = line.strip().split(',', 1)
                if user == username: #Verify the [assword if the username matches
                    return verify_password(password, hash)
    except FileNotFoundError: #Error if file is not found
        print("No users registered yet.") #Printing error message to indicate that users has not registered yet
        return False
    return False

#Function to validate username
def validate_username(username):
    if len(username) < 3: #Checks if the the username is atleast 3 characters long
        return False, "Username must be at least 3 characters long." #
    if "," in username: #Checks if username contains comma
        return False, "Username cannot contain commas." #Return false if username contains comma
    return True, ""

#Function to validate password
def validate_password(password):
    if len(password) < 6: #Checks if the password is at least 4 character lengths long
        return False, "Password must be at least 6 characters long."
    if password.isalpha() or password.isdigit(): #checks if passwords contains both letters and digits
        return False, "Password must contain both letters and numbers." #Return false and error message if there is only letters or digits
    return True, ""

#Function to display the main menu option
def display_menu():
    #Printing header and menu options
    print("\n" + "=" * 50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM") #Main title
    print("Secure Authentication System") #System title
    print("=" * 50)
    print("\n[1] Register a new user") #Register function
    print("[2] Login") #Loging function
    print("[3] Exit") #Exit function
    print("-" * 50)

#Function to run the authentication system
def main():
    print("\nWelcome to the Week 7 Authentication System!") #Print success message
    while True: #Allow applications to keep running until users wants to exit
        display_menu() #Display the menu option
        choice = input("\nPlease select an option (1-3): ").strip() #Allow user to choose between option 1 to 3

        if choice == "1": #Register user
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username) #Validate username
            if not is_valid:
                print(f"Error: {error_msg}") #Print error message if username is not valid
                continue #Restart to allow the user to try again

            password = input("Enter a password: ").strip() #Prompts password from the user
            is_valid, error_msg = validate_password(password) #Validate password
            if not is_valid:
                print(f"Error: {error_msg}") #Print error message if password is not valid
                continue #Restart the process to allow the user to try again

            password_confirm = input("Confirm password: ").strip() #confirm password from the user
            if password != password_confirm: #Compare password with the original password
                print("Error: Passwords do not match.") #Error message if password does not match
                continue

            register_user(username, password)

        elif choice == "2": #Login user
            print("\n--- LOGIN ---")
            #Prompts user for login credentials
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            #Indicates login successful
            if login_user(username, password):
                print("\nYou are now logged in.")
                input("\nPress Enter to return to main menu.")
            else: #Error message if login failed
                print("Error: Invalid username or password.")

        elif choice == "3": #Exit option
            print("\nThank you for using the Authentication System") #Print thank you message
            print("Exiting...") #Displaying exit function
            break #Break the loop from the authentication system

        else:
            print("\nError: Invalid Option. Please select option 1, 2 or 3.") #Print error message

if __name__ == "__main__": #Controls the script execution
    main()