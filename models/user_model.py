from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
users_collection = db["users"]

def create_user(user_data):
    users_collection.insert_one(user_data)

def find_user_by_username(username):
    return users_collection.find_one({"username": username})

def make_admin(username):
    users_collection.update_one(
        {"username": username},
        {"$set": {"role": "admin"}}
    )