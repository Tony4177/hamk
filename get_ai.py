def get_ai_response(question):
    question = question.lower()

    if "miss dose" in question:
        return "If you miss a dose, take it as soon as you remember. If it's almost time for next dose, skip the missed one."

    elif "side effect" in question:
        return "Common side effects depend on the medicine. Please consult a doctor for accurate advice."

    elif "when" in question and "medicine" in question:
        return "You can check your scheduled medicines in the dashboard."

    elif "safe" in question:
        return "Medicine safety depends on dosage and health conditions. Always follow doctor's advice."

    else:
        return "I am your medicine assistant. Ask me about dosage, missed doses, or safety."