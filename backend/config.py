import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_ID = int(os.getenv('API_ID'))
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    YOUTUBE_KEY = os.getenv('YOUTUBE_API_KEY')
    LASTFM_KEY = os.getenv('LASTFM_API_KEY')
    WEBAPP_URL = os.getenv('WEBAPP_URL')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))
    PUBLIC_TOKEN = os.getenv('API_PUBLIC_TOKEN')
    API_BASE = f"http://{HOST}:{PORT}"

settings = Settings()