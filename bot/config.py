import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')
DEFAULT_BOT_LANGUAGE = os.getenv('DEFAULT_BOT_LANGUAGE')
