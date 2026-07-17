import json

def login():
    with open("Users.json", "r") as file:
        users = json.load(file)

    print("===== QUANTUM MIND AI =====")
    print("Private Softnet Technology Academy AI")
    print()

    username = input("Username: ")
    password = input("Password: ")

    if username in users:
        if users[username]["password"] == password:
            print("\nAccess Granted!\n")
            return username, users[username]["role"]

    print("\nAccess Denied!")
    print("Quantum Mind is only for Softnet Technology Academy students and teachers.")
    return None, None
