import os
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

load_dotenv()

class ActionGeminiChat(Action):
    def name(self) -> str:
        return "action_gemini_chat"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        user_message = tracker.latest_message.get("text")
        api_key = os.getenv("GEMINI_API_KEY")
        url = "https://api.gemini.ai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gemini-pro-v1",
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 150,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=20)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
        except Exception:
            answer = "Kuch problem aa gayi hai, plz try karo baad me."

        dispatcher.utter_message(text=answer)
        return []
