import bcrypt
import os

USER_DATA_FILE = "Users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')  # store as string

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password):
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password}\n")
    print(f"User '{username}' registered successfully")
    return True

def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                user, _ = line.strip().split(',', 1)
                if user == username:
                    return True
    except FileNotFoundError:
        return False
    return False

def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f.readlines():
                user, hash = line.strip().split(',', 1)
                if user == username:
                    return verify_password(password, hash)
    except FileNotFoundError:
        print("No users registered yet.")
        return False
    return False

def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if "," in username:
        return False, "Username cannot contain commas."
    return True, ""

def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if password.isalpha() or password.isdigit():
        return False, "Password must contain both letters and numbers."
    return True, ""

def display_menu():
    print("\n" + "=" * 50)
    print("MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("Secure Authentication System")
    print("=" * 50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-" * 50)

def main():
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == "1":
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            print("\n--- LOGIN ---")
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()

            if login_user(username, password):
                print("\nYou are now logged in.")
                input("\nPress Enter to return to main menu.")
            else:
                print("Error: Invalid username or password.")

        elif choice == "3":
            print("\nThank you for using the Authentication System")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid Option. Please select option 1, 2 or 3.")

if __name__ == "__main__":
    main()