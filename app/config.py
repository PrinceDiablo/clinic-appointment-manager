import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file (so environment variables are ready.)
load_dotenv()

class Config:
    # Flask core settings
    SECRET_KEY = os.getenv("FLASK_SECRET")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Session settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # Security settings
    MAX_FAILED_LOGINS = 5
    LOCKOUT_DURATION = timedelta(minutes=5)

    # --- Database settings ---
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "clinic")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "clinicdb")