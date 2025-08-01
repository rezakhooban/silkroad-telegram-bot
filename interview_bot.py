import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from dotenv import load_dotenv
from flask import Flask, request
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # مثل: https://yourapp.onrender.com/webhook
PORT = int(os.getenv("PORT", 8443))

(START, NAME, ORG, ROLE, EXP, INTERVIEW) = range(6)

questions = [
    # لیست سوالات مشابه قبل
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("تکمیل اطلاعات")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی ...",
        reply_markup=markup,
    )
    return START

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("نام و نام خانوادگی:")
    return NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("ارگان محل خدمت:\n☑ دولتی\t☑ خصوصی")
    return ORG

async def handle_org(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["org"] = update.message.text
    await update.message.reply_text("جایگاه سازمانی:\n☑ کارشناس\t☑ مدیر میانی\t☑ مدیر ارشد")
    return ROLE

async def handle_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["role"] = update.message.text
    await update.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد:\n☑ بله\t☑ خیر")
    return EXP

async def handle_exp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["exp"] = update.message.text
    await update.message.reply_text(
        "برای شروع مصاحبه، دکمه زیر را فشار دهید.",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("شروع مصاحبه")]], resize_keyboard=True),
    )
    context.user_data["q_index"] = 0
    return INTERVIEW

async def handle_interview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data.get("q_index", 0)
    await update.message.reply_text(questions[index])
    return INTERVIEW

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data.get("q_index", 0)
    name = context.user_data.get("name", "بدون‌نام")
    admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))  # عددی، نه @username

    if update.message.voice:
        await context.bot.send_voice(chat_id=admin_chat_id, voice=update.message.voice.file_id,
                                     caption=f"\U0001F464 {name}\nپاسخ سوال {index + 1}:")

    index += 1
    if index < len(questions):
        context.user_data["q_index"] = index
        await update.message.reply_text(questions[index])
        return INTERVIEW
    else:
        await update.message.reply_text("✅ مصاحبه به پایان رسید. سپاس از مشارکت شما.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("مصاحبه لغو شد.")
    return ConversationHandler.END

# ساخت اپلیکیشن تلگرام
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [MessageHandler(filters.Regex("^(تکمیل اطلاعات)$"), handle_start_button)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
        ORG: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_org)],
        ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_role)],
        EXP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_exp)],
        INTERVIEW: [
            MessageHandler(filters.Regex("^(شروع مصاحبه)$"), handle_interview),
            MessageHandler(filters.VOICE, handle_voice)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

# اجرای webhook
async def main():
    await app.initialize()
    await app.start()
    await app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook set!")

flask_app = Flask(__name__)

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    asyncio.run(app.process_update(update))
    return "OK"

if __name__ == "__main__":
    asyncio.run(main())
    flask_app.run(host="0.0.0.0", port=PORT)
