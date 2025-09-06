from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

ORDERS_DB = {
    "12345": "Your order #12345 is being processed and will be delivered in 3 days.",
    "54321": "Order #54321 has been shipped and is out for delivery.",
    "11223": "Order #11223 was delivered yesterday.",
}

class ActionOrderStatus(Action):

    def name(self) -> Text:
        return "action_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")

        if order_id and order_id in ORDERS_DB:
            dispatcher.utter_message(text=ORDERS_DB[order_id])
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find that order ID. Please try again.")

        return []
