from dotenv import load_dotenv
import os
load_dotenv()  # loads variables from .env into environment
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionHuggingFaceChat(Action):
    def name(self):
        return "action_huggingface_chat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        user_message = tracker.latest_message.get('text')
        api_key = "YOUR_HUGGINGFACE_API_KEY"  # ← Replace here
        model_name = "microsoft/DialoGPT-medium"
        api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": user_message,
            "parameters": {
                "max_length": 200,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and result:
                answer = result[0].get('generated_text', '')
                if user_message in answer:
                    answer = answer.replace(user_message, "").strip()
            else:
                answer = "मैं अभी सीख रहा हूँ, थोड़ी देर बाद बेहतर जवाब दूंगा।"
        except:
            answer = "Sorry, कुछ technical issue है।"
        dispatcher.utter_message(text=answer)
        return []
