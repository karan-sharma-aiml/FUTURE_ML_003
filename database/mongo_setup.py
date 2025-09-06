from pymongo import MongoClient
from backend.config import MONGO_URI

def get_mongo_client():
    client = MongoClient(MONGO_URI)
    db = client["chatbot"]
    return db
