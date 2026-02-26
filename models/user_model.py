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


def delete_user(username):
    """Remove a user document from the database."""
    users_collection.delete_one({"username": username})


def get_all_users():
    """Return all users (passwords excluded)."""
    cursor = users_collection.find({}, {"_id": 0, "password": 0})
    return list(cursor)