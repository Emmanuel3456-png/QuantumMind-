def answer(question):

    question = question.lower()

    if "principal" in question:
        return "Please update this answer with your school's principal."

    elif "academy" in question:
        return "Softnet Technology Academy is a technology-focused learning institution."

    elif "courses" in question:
        return "Please update this answer with the courses offered by the academy."

    elif "computer studies" in question:
        return "Computer Studies teaches the fundamentals of computers, software, and programming."

    return None
