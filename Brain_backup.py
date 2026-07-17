from datetime import datetime
from database import (
    load_knowledge,
    save_knowledge,
    load_settings,
    load_memory,
    save_memory
)

knowledge = load_knowledge()
settings = load_settings()
memory = load_memory()


def show_help():
    print("""
===============================
       QUANTUM MIND HELP
===============================
help
time
date
calculate 5+7
who created you
who can use you
bye
===============================
""")


def calculate(expression):
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except:
        return "Invalid calculation."


def chat(username, role):

    print("\n===============================")
    print("     QUANTUM MIND AI")
    print("===============================")
    print(f"Welcome {username}")
    print(f"Role: {role}")
    print(f"Academy: {settings['academy']}")
    print("===============================")

    while True:

        user = input("\nYou: ").lower().strip()

        if user == "":
            continue

        if user == "bye":
            print("Quantum Mind: Goodbye!")
            break

        elif user == "help":
            show_help()

        elif user == "time":
            print("Quantum Mind:", datetime.now().strftime("%I:%M %p"))

        elif user == "date":
            print("Quantum Mind:", datetime.now().strftime("%d %B %Y"))

        elif user.startswith("calculate"):

            expression = user.replace("calculate", "").strip()

            print("Quantum Mind:", calculate(expression))
        elif user == "who created you":
            print(f"Quantum Mind: I was created by {settings['creator']}.")

        elif user == "who can use you":
            print(f"Quantum Mind: I am the private AI assistant of {settings['academy']}.")
            print("Only authorized pupils, teachers and administrators should use me.")

        elif user.startswith("remember "):

            text = user.replace("remember", "", 1).strip()

            if ":" in text:

                key, value = text.split(":", 1)

                memory[key.strip().lower()] = value.strip()

                save_memory(memory)

                print("Quantum Mind: I will remember that.")

            else:

                print("Quantum Mind: Use this format:")

                print("remember favourite colour: blue")

        elif user.startswith("what is my "):

            key = user.replace("what is my", "", 1).strip()

            if key in memory:

                print("Quantum Mind:", memory[key])

            else:

                print("Quantum Mind: I don't know that yet.")

        else:

            found = False

            for question, answer in knowledge.items():

                question_words = set(question.lower().split())
                user_words = set(user.lower().split())

                if question_words.intersection(user_words):

                    print("Quantum Mind:", answer)

                    found = True

                    break

            if not found:

                print("Quantum Mind: I don't know the answer.")

                teach = input("Can you teach me? (yes/no): ").lower()

                if teach == "yes":

                    answer = input("Enter the answer: ")

                    knowledge[user] = answer

                    save_knowledge(knowledge)

                    print("Quantum Mind: Thank you! I have learned something new.")

                else:

                    print("Quantum Mind: Okay, maybe next time.")
