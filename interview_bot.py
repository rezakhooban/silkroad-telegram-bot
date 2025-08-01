import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from aiofiles import open as aio_open

# فعال کردن لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مراحل گفت‌وگو
(START, FULLNAME, ORGAN, POSITION, EXPERIENCE, INTRO, INTERVIEW) = range(7)

# سوالات مصاحبه
QUESTIONS = [
    "1. از منظر شما، شهرداری قزوین با چه اهداف کلان و راهبردی به برگزاری اجلاس بین‌المللی شهرداران جاده ابریشم مبادرت ورزید و این اهداف چه نسبتی با رویکردهای نوین در روابط عمومی دارد؟",
    "2. روابط عمومی شهرداری قزوین در کدامین سطوح عملیاتی—از مرحله طراحی تا اجرا—بیشترین نقش را ایفا کرده و این نقش‌آفرینی در کدام الگوی نظری قابل صورت‌بندی است؟",
    "3. چه ابزارها و بسترهایی در حوزه رسانه‌های سنتی، دیجیتال و محیطی برای پوشش این رویداد به‌کار گرفته شد و چه منطق ارتباطی بر انتخاب آن‌ها حاکم بوده است؟",
    "4. تا چه اندازه از عناصر نمادین، روایت‌های فرهنگی و نشانه‌های بومی برای بازنمایی هویت فرهنگی شهر قزوین در ساختار رویداد استفاده شد و این عناصر چگونه رمزگذاری فرهنگی صورت گرفته‌اند؟",
    "5. بازخورد مخاطبان ملی و بین‌المللی نسبت به چهره فرهنگی بازنمایی‌شده از شهر قزوین چه بوده است و این بازخوردها چگونه در ارزیابی عملکرد روابط عمومی قابل تحلیل‌اند؟",
    "6. در فرایند اجرا یا روایت‌سازی فرهنگی اجلاس، با چه چالش‌ها یا گسست‌هایی مواجه بودید و سازوکار مواجهه یا مدیریت آن‌ها از چه رویکردهایی تبعیت می‌کرد؟",
    "7. روابط عمومی شهرداری چگونه توانست در سطح بین‌فرهنگی و فراملی با شهرداران، نهادهای بین‌المللی و کنشگران فرهنگی تعامل مؤثر برقرار سازد؟",
    "8. از منظر شما، کدام تجربه‌ها و دستاوردهای این رویداد می‌تواند برای شهرداری‌های دیگر در حوزه برندسازی فرهنگی و دیپلماسی شهری الگوبخش باشد؟",
    "9. آیا در تولید محتوا، روایت‌سازی یا بازنمایی رسانه‌ای، از چارچوب‌های نظری مشخصی بهره گرفته شد؟ اگر بله، چه مدل یا الگویی مورد استفاده قرار گرفت؟",
    "10. چه پیشنهادهایی برای ارتقاء سطح راهبردی، روایی یا ارتباطی روابط عمومی شهرداری قزوین در مواجهه با رویدادهای آتی فرهنگی دارید؟"
]

user_responses = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    user_responses[chat_id] = {}

    await update.message.reply_text(
        "این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی از طریق اجلاس بین‌المللی شهرداران جاده ابریشم طراحی شده است.\n\nمشارکت شما در پاسخ به این مصاحبه، در مسیر توسعه برنامه‌های فرهنگی آینده کمک شایانی خواهد کرد.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("تکمیل اطلاعات")]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return START

async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("نام و نام خانوادگی:")
    return FULLNAME

async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    user_responses[chat_id]['fullname'] = update.message.text

    await update.message.reply_text("ارگان محل خدمت: \n☐ دولتی \t ☐ خصوصی")
    return ORGAN

async def save_organ(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    user_responses[chat_id]['organ'] = update.message.text

    await update.message.reply_text("جایگاه سازمانی: \n☐ کارشناس \t ☐ مدیر میانی \t ☐ مدیر ارشد")
    return POSITION

async def save_position(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    user_responses[chat_id]['position'] = update.message.text

    await update.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد؟ ☐ بله \t ☐ خیر")
    return EXPERIENCE

async def save_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    user_responses[chat_id]['experience'] = update.message.text

    await update.message.reply_text(
        "با انجام این مصاحبه، گامی موثر در مسیر هويت‌سازی (برندسازی) فرهنگ شهری قزوین برمی‌دارید.\n\nراهنما: با ظاهر شدن سوال، می‌توانید صدای خود را در پاسخ ضبط و ارسال کنید.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("شروع مصاحبه")]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return INTRO

async def start_interview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(QUESTIONS[0])
    context.user_data['q_index'] = 0
    return INTERVIEW

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    q_idx = context.user_data.get('q_index', 0)

    voice_file = await update.message.voice.get_file()
    file_path = f"voice_{chat_id}_{q_idx}.ogg"
    await voice_file.download_to_drive(file_path)

    # ارسال به آیدی ذخیره‌سازی
    try:
        with open(file_path, 'rb') as f:
            await context.bot.send_voice(chat_id='@rezakhooban', voice=InputFile(f), caption=f"پاسخ کاربر: {user_responses[chat_id].get('fullname', '')}\nسوال {q_idx + 1}:\n{QUESTIONS[q_idx]}")
    except Exception as e:
        logger.error(f"ارسال ویس به آیدی شکست خورد: {e}")

    q_idx += 1
    if q_idx < len(QUESTIONS):
        context.user_data['q_index'] = q_idx
        await update.message.reply_text(QUESTIONS[q_idx])
        return INTERVIEW
    else:
        await update.message.reply_text("پایان مصاحبه. سپاس از همکاری شما.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("مصاحبه لغو شد.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TOKEN", "8209512056:AAEfFgOISrub-n8KdaoEusAEj7d_55LZCkI")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(filters.TEXT & filters.Regex("تکمیل اطلاعات"), collect_name)],
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_name)],
            ORGAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_organ)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_position)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_experience)],
            INTRO: [MessageHandler(filters.TEXT & filters.Regex("شروع مصاحبه"), start_interview)],
            INTERVIEW: [MessageHandler(filters.VOICE, handle_voice)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    print("Bot is polling...")
    app.run_polling()
