from utils.security import hash_password, verify_password
from models.user_model import create_user, find_user_by_username

def register_user(data):
    if find_user_by_username(data["username"]):
        return False, "User already exists"

    data["password"] = hash_password(data["password"])
    data["role"] = "user"

    create_user(data)
    return True, "User registered"

def login_user(username, password):
    user = find_user_by_username(username)
    if user and verify_password(user["password"], password):
        return True, user
    return False, None