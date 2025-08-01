# interview_bot.py

import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

(START, NAME, ORG, ROLE, EXP, INTERVIEW) = range(6)

questions = [
    "1. از منظر شما، شهرداری قزوین با چه اهداف کلان و راهبردی به برگزاری اجلاس بین‌المللی شهرداران جاده ابریشم مبادرت ورزید و این اهداف چه نسبتی با رویکردهای نوین در روابط عمومی دارد؟",
    "2. روابط عمومی شهرداری قزوین در کدامین سطوح عملیاتی از مرحله طراحی تا اجرا بیشترین نقش را ایفا کرده و این نقش‌آفرینی در کدام الگوی نظری قابل صورت‌بندی است؟",
    "3. چه ابزارهایی در حوزه رسانه‌های سنتی، دیجیتال و محیطی برای پوشش این رویداد به کار گرفته شد و چه منطق ارتباطی بر انتخاب آن‌ها حاکم بوده است؟",
    "4. تا چه اندازه از عناصر نمادین، روایت‌های فرهنگی و نشانه‌های بومی برای بازنمایی هویت فرهنگی شهر قزوین در ساختار رویداد استفاده شد؟",
    "5. بازخورد مخاطبان ملی و بین‌المللی نسبت به چهره فرهنگی بازنمایی‌شده از شهر قزوین چه بوده است؟",
    "6. در فرایند اجرا یا روایت‌سازی فرهنگی اجلاس، با چه چالش‌ها یا گسست‌هایی مواجه بودید و چگونه مدیریت شد؟",
    "7. روابط عمومی شهرداری چگونه توانست در سطح بین‌فرهنگی و فراملی با نهادها و شهرداران تعامل مؤثر برقرار سازد؟",
    "8. چه تجربه‌ها و دستاوردهایی از این رویداد برای شهرداری‌های دیگر الگوبخش است؟",
    "9. آیا در روایت‌سازی رسانه‌ای، از چارچوب‌های نظری مشخصی استفاده شد؟ اگر بله، چه الگویی؟",
    "10. چه پیشنهادهایی برای ارتقای سطح روایی و ارتباطی روابط عمومی شهرداری قزوین در مواجهه با رویدادهای آتی دارید؟"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("تکمیل اطلاعات")]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی "
        "از طریق اجلاس بین‌المللی شهرداران جاده ابریشم طراحی شده است.\n\n"
        "مشارکت شما در پاسخ به این مصاحبه، در مسیر توسعه برنامه‌های فرهنگی آینده کمک شایانی خواهد کرد.",
        reply_markup=markup,
    )
    return START

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("نام و نام خانوادگی:")
    return NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("ارگان محل خدمت:\n☐ دولتی\t☐ خصوصی")
    return ORG

async def handle_org(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["org"] = update.message.text
    await update.message.reply_text("جایگاه سازمانی:\n☐ کارشناس\t☐ مدیر میانی\t☐ مدیر ارشد")
    return ROLE

async def handle_role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["role"] = update.message.text
    await update.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد:\n☐ بله\t☐ خیر")
    return EXP

async def handle_exp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["exp"] = update.message.text
    await update.message.reply_text(
        "با انجام این مصاحبه، گامی موثر در مسیر هويت‌سازی (برندسازی) فرهنگ شهری قزوین برمی‌دارید.\n"
        "راهنما: با ظاهر شدن سوال، شما می‌توانید صدای خود را در پاسخ به سوال ضبط و ارسال کنید.\n\n"
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
    admin_chat_id = "@rezakhooban"

    caption = f"\U0001F464 {name}\nپاسخ سوال {index + 1}:\n"
    if update.message.voice:
        await context.bot.send_voice(chat_id=admin_chat_id, voice=update.message.voice.file_id, caption=caption)

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

def main():
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
    print("🔄 Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
