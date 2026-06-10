import os
import logging
from telegram.ext import ApplicationBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://api:8000")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    logging.info("Bot iniciado...")
    app.run_polling()
