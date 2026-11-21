
import json
import os
import string
import secrets
from cryptography.fernet import Fernet

KEY_FILE = "key.key"
ENCRYPTED_FILE = "passwords.enc"
OLD_FILE = "passwords.json"

# Create or load encryption key
if not os.path.exists(KEY_FILE):
    if os.path.exists(ENCRYPTED_FILE):
        raise FileNotFoundError("Encryption key is missing!")

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as file:
        file.write(key)
else:
    with open(KEY_FILE, "rb") as file:
        key = file.read()

fernet = Fernet(key)


# Load saved passwords
if os.path.exists(ENCRYPTED_FILE):

    with open(ENCRYPTED_FILE, "rb") as file:
        encrypted_data = file.read()

    passwords = json.loads(
        fernet.decrypt(encrypted_data).decode()
    )

elif os.path.exists(OLD_FILE):

    with open(OLD_FILE, "r") as file:
        passwords = json.load(file)

else:
    passwords = []


# Save passwords with encryption
def save_passwords():

    data = json.dumps(passwords).encode()
    encrypted_data = fernet.encrypt(data)

    with open(ENCRYPTED_FILE, "wb") as file:
        file.write(encrypted_data)


# Generate a strong password
def generate_password():

    characters = string.ascii_letters + string.digits + "!@#$%&*"

    password = "".join(
        secrets.choice(characters) for _ in range(16)
    )

    return password


# Start the application
print("Welcome to Secure Password Manager!")

print("\nTo start the app, write 'start'")

start = input("Enter: ")

while start.lower() != "start":
    print("Invalid command! Please write 'start'.")
    start = input("Enter: ")


# Main menu
while True:

    print("\n========== MENU ==========")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Search Password")
    print("4. Delete Password")
    print("5. Generate Password")
    print("6. Exit")

    choice = input("Choose an option: ")

    # Add Password
    if choice == "1":

        website = input("Enter website name: ")
        password = input("Enter password: ")

        if not website.strip() or not password.strip():
            print("Website and password cannot be empty!")

        else:
            passwords.append({
                "website": website,
                "password": password
            })

            save_passwords()
            print("Password added successfully!")

    # View Passwords
    elif choice == "2":

        if not passwords:
            print("No passwords saved.")

        else:
            print("\nYour Saved Passwords:")

            for item in passwords:
                print(item["website"], ":", item["password"])

            print("Total Saved Passwords:", len(passwords))

    # Search Password
    elif choice == "3":

        search = input("Enter website name: ")
        found = False

        for item in passwords:
            if item["website"].lower() == search.lower():
                print("Password:", item["password"])
                found = True

        if not found:
            print("Website not found.")

    # Delete Password
    elif choice == "4":

        website = input("Enter website to delete: ")
        found = False

        for item in passwords:
            if item["website"].lower() == website.lower():
                passwords.remove(item)
                save_passwords()
                print("Password deleted successfully!")
                found = True
                break

        if not found:
            print("Website not found.")

    # Generate Password
    elif choice == "5":

        new_password = generate_password()

        print("\nGenerated Password:")
        print(new_password)

        save_choice = input("Save this password? (yes/no): ")

        if save_choice.lower() == "yes":

            website = input("Enter website name: ")

            if not website.strip():
                print("Website cannot be empty!")

            else:
                passwords.append({
                    "website": website,
                    "password": new_password
                })

                save_passwords()
                print("Password saved successfully!")

    # Exit
    elif choice == "6":

        print("Goodbye!")
        break

    else:
        print("Invalid option!")
