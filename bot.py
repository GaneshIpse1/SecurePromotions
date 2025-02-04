import logging
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7701313809:AAFA-cotOTczC0KcYDdlRj7fQuYWxDRSZpA"
WEB_SERVER_URL = "https://yourserver.com"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me a link, and I'll secure it for you!")

async def secure_link(update: Update, context: CallbackContext):
    original_link = update.message.text.strip()

    if not (original_link.startswith("http://") or original_link.startswith("https://")):
        await update.message.reply_text("Please send a valid link (starting with http:// or https://).")
        return

    response = requests.post(f"{WEB_SERVER_URL}/generate", json={"link": original_link})

    if response.status_code == 200:
        webview_link = response.json()["masked_link"]
        keyboard = [[InlineKeyboardButton("Open Secure Link", web_app=webview_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Click below to access the secured link:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Error generating secured link. Try again later.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, secure_link))
    app.run_polling()

if __name__ == "__main__":
    main()