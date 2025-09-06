# Utility functions for chatbot backend

def clean_text(text):
    return text.strip().lower()

def format_response(response):
    return {"reply": response}

def validate_input(user_input):
    if not user_input or len(user_input) < 2:
        raise ValueError("Input too short.")
    return True
