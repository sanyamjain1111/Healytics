
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY="AIzaSyDJsa6J8hYaVnTVaJYKRcqZsgjHnFuxF90"
DATABASE_URL="postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
APP_ENV="development"

class Settings:
    GEMINI_API_KEY = "AIzaSyDJsa6J8hYaVnTVaJYKRcqZsgjHnFuxF90"
    DATABASE_URL = "postgresql+psycopg2://postgres:Jain%402514@127.0.0.1:5432/med_ai"
    APP_ENV = "development"

settings = Settings()
