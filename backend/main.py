from fastapi import FastAPI
from pydantic import BaseModel
from database.save_chat import log_chat  # Ensure this module exists and works
import requests

app = FastAPI()

class Query(BaseModel):
    user_id: str
    text: str

def get_bot_response(user_id: str, user_msg: str) -> str:
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": user_id, "message": user_msg}
    try:
        response = requests.post(rasa_url, json=payload, timeout=5)
        response.raise_for_status()  # Raise error for bad HTTP status codes
        data = response.json()  # Expected: list of dicts
        if data and "text" in data[0]:
            return data[0]["text"]
        else:
            return "Sorry, I didn't understand that."
    except Exception as e:
        return f"Error communicating with chatbot: {str(e)}"

@app.post("/chat")
def chat(query: Query):
    bot_reply = get_bot_response(query.user_id, query.text)
    if not bot_reply:
        bot_reply = "Sorry, I didn't get that."
    # Log chat to MongoDB (optional, ensure your function works)
    log_chat(query.user_id, query.text, bot_reply)
    return {"user": query.text, "bot": bot_reply}
