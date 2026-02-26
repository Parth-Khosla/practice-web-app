import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    ADMIN_URL_SECRET = os.getenv("ADMIN_URL_SECRET")

    # timeout for permanent sessions in seconds; default to 120 if unset
    SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "120"))
    # Flask's default behavior is to refresh the expiration each request
    # which made our timeout appear to never happen when the user was active.
    # We'll disable that and enforce inactivity in a before_request handler.
    SESSION_REFRESH_EACH_REQUEST = False

    # initial admin credentials (first run only) pulled from environment
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@123")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PHONE = os.getenv("ADMIN_PHONE", "0000000000")