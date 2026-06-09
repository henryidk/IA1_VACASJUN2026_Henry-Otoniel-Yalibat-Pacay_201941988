import os
from dotenv import load_dotenv

load_dotenv()

FLASK_PORT       = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG      = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
HISTORY_PATH     = os.getenv('HISTORY_PATH', '/data/historial.json')
TELEGRAM_TOKEN   = os.getenv('TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
PROLOG_FILE      = os.path.join(os.path.dirname(__file__), 'prolog', 'base_conocimiento.pl')
