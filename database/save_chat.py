from database.mongo_setup import get_mongo_client

def log_chat(user_id, user_input, bot_response):
    db = get_mongo_client()
    chat_log = {
        "user_id": user_id,
        "user_input": user_input,
        "bot_response": bot_response
    }
    db.chats.insert_one(chat_log)
    return True
