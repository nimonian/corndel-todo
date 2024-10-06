import os
from dotenv import load_dotenv

MODE = os.getenv("MODE", "development")
load_dotenv(f".env.{MODE}")

PORT = int(os.getenv("PORT", 5000))
DEBUG = MODE in ["development", "testing"]
TESTING = MODE == "testing"
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
