import os
import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://api:8000")


async def handle_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    usuario = update.message.from_user.username or update.message.from_user.first_name

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{API_URL}/consulta", params={"q": texto})
            data = response.json()
        await update.message.reply_text(data["respuesta"])
    except httpx.RequestError:
        logging.error(f"No se pudo conectar a la API para consulta de: {usuario}")
        await update.message.reply_text("El servicio no está disponible en este momento. Intenta más tarde.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        await update.message.reply_text("Ocurrió un error al procesar tu consulta. Intenta de nuevo.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mensaje))
    logging.info("Bot iniciado y escuchando mensajes...")
    app.run_polling()
