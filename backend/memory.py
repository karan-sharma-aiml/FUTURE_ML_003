conversation_history = {}

def update_memory(user_id, user_input, bot_response):
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"user": user_input, "bot": bot_response})
    return conversation_history[user_id]

def get_memory(user_id):
    return conversation_history.get(user_id, [])
