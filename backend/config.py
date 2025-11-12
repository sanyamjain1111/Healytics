
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY="AIzaSyCD3uRdPVzZM2G2Emrdfc2g5CzoBv29oSU"
DATABASE_URL="postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
APP_ENV="development"

class Settings:
    GEMINI_API_KEY = "AIzaSyCD3uRdPVzZM2G2Emrdfc2g5CzoBv29oSU"
    DATABASE_URL = "postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
    APP_ENV = "development"
    # --- JWT ---
    JWT_SECRET: str = "healytics12121"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MIN: int = 120
    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str = "57926672783-6d4vr7f7ec7bjrspqbpoehcfrvdh06hp.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str = "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"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:5173"

settings = Settings()
