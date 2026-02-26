import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    ADMIN_URL_SECRET = os.getenv("ADMIN_URL_SECRET")
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT"))