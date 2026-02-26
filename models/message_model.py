from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
messages_collection = db["messages"]

def create_message(data):
    messages_collection.insert_one(data)

def get_user_messages(username):
    return list(messages_collection.find({"username": username}))