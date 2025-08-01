import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    if not voice:
        await update.message.reply_text("فایل صوتی دریافت نشد.")
        return
    file = await context.bot.get_file(voice.file_id)
    file_path = "voice_message.ogg"
    await file.download_to_drive(file_path)
    await update.message.reply_text("فایل صوتی دریافت و ذخیره شد.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("ربات فعال است...")
    app.run_polling()

if __name__ == "__main__":
    main()