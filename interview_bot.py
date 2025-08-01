import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (ApplicationBuilder, ContextTypes, MessageHandler, filters,
                          CommandHandler, ConversationHandler, CallbackQueryHandler)

logging.basicConfig(level=logging.INFO)

# States
NAME, ORG_TYPE, POSITION, EXPERIENCE, INTRO_DONE, INTERVIEW = range(6)

TOKEN = os.getenv("BOT_TOKEN", "8209512056:AAEfFgOISrub-n8KdaoEusAEj7d_55LZCkI")
ADMIN_USERNAME = "rezakhooban"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی از طریق اجلاس بین‌المللی شهرداران جاده ابریشم طراحی شده است.

مشارکت شما در پاسخ به این مصاحبه، در مسیر توسعه برنامه‌های فرهنگی آینده کمک شایانی خواهد کرد.""",
        reply_markup=ReplyKeyboardMarkup([["تکمیل اطلاعات"]], resize_keyboard=True)
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("ارگان محل خدمت:", reply_markup=ReplyKeyboardMarkup(
        [["دولتی", "خصوصی"]], resize_keyboard=True))
    return ORG_TYPE

async def get_org(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['org'] = update.message.text
    await update.message.reply_text("جایگاه سازمانی:", reply_markup=ReplyKeyboardMarkup(
        [["کارشناس", "مدیر میانی", "مدیر ارشد"]], resize_keyboard=True))
    return POSITION

async def get_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['position'] = update.message.text
    await update.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد:", reply_markup=ReplyKeyboardMarkup(
        [["بله", "خیر"]], resize_keyboard=True))
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['experience'] = update.message.text

    await update.message.reply_text(
        """با انجام این مصاحبه، گامی موثر در مسیر هويت سازي (برندسازي) فرهنگ شهري قزوین برمی دارید.
راهنما: با ظاهر شدن سوال شما می توانید صدای خود را در پاسخ به سوال ضبط و ارسال کنید.""",
        reply_markup=ReplyKeyboardMarkup([["شروع مصاحبه"]], resize_keyboard=True))
    return INTRO_DONE

QUESTIONS = [
    "از منظر شما، شهرداری قزوین با چه اهداف کلان و راهبردی به برگزاری اجلاس بین‌المللی شهرداران جاده ابریشم مبادرت ورزید و این اهداف چه نسبتی با رویکردهای نوین در روابط عمومی دارد؟",
    "روابط عمومی شهرداری قزوین در کدامین سطوح عملیاتی—از مرحله طراحی تا اجرا—بیشترین نقش را ایفا کرده و این نقش‌آفرینی در کدام الگوی نظری قابل صورت‌بندی است؟",
    "چه ابزارها و بسترهایی در حوزه رسانه‌های سنتی، دیجیتال و محیطی برای پوشش این رویداد به‌کار گرفته شد و چه منطق ارتباطی بر انتخاب آن‌ها حاکم بوده است؟",
    "تا چه اندازه از عناصر نمادین، روایت‌های فرهنگی و نشانه‌های بومی برای بازنمایی هویت فرهنگی شهر قزوین در ساختار رویداد استفاده شد و این عناصر چگونه رمزگذاری فرهنگی صورت گرفته‌اند؟",
    "بازخورد مخاطبان ملی و بین‌المللی نسبت به چهره فرهنگی بازنمایی‌شده از شهر قزوین چه بوده است و این بازخوردها چگونه در ارزیابی عملکرد روابط عمومی قابل تحلیل‌اند؟",
    "در فرایند اجرا یا روایت‌سازی فرهنگی اجلاس، با چه چالش‌ها یا گسست‌هایی مواجه بودید و سازوکار مواجهه یا مدیریت آن‌ها از چه رویکردهایی تبعیت می‌کرد؟",
    "روابط عمومی شهرداری چگونه توانست در سطح بین‌فرهنگی و فراملی با شهرداران، نهادهای بین‌المللی و کنشگران فرهنگی تعامل مؤثر برقرار سازد؟",
    "از منظر شما، کدام تجربه‌ها و دستاوردهای این رویداد می‌تواند برای شهرداری‌های دیگر در حوزه برندسازی فرهنگی و دیپلماسی شهری الگوبخش باشد؟",
    "آیا در تولید محتوا، روایت‌سازی یا بازنمایی رسانه‌ای، از چارچوب‌های نظری مشخصی بهره گرفته شد؟ اگر بله، چه مدل یا الگویی مورد استفاده قرار گرفت؟",
    "چه پیشنهادهایی برای ارتقاء سطح راهبردی، روایی یا ارتباطی روابط عمومی شهرداری قزوین در مواجهه با رویدادهای آتی فرهنگی دارید؟"
]

async def intro_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q'] = 0
    await update.message.reply_text(f"سوال ۱:
{QUESTIONS[0]}")
    return INTERVIEW

async def collect_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = context.user_data.get('q', 0)
    user = update.effective_user

    # دریافت فایل صوتی و ارسال به ادمین
    if update.message.voice:
        file = await update.message.voice.get_file()
        caption = f"👤 {user.full_name}  | سوال {q+1}\n@{user.username or '-'}"
        await context.bot.send_voice(chat_id=f"@{ADMIN_USERNAME}", voice=file.file_id, caption=caption)

        q += 1
        if q < len(QUESTIONS):
            context.user_data['q'] = q
            await update.message.reply_text(f"سوال {q+1}:
{QUESTIONS[q]}")
            return INTERVIEW
        else:
            await update.message.reply_text("✅ مصاحبه به پایان رسید. سپاسگزاریم.")
            return ConversationHandler.END
    else:
        await update.message.reply_text("لطفاً پاسخ را به صورت پیام صوتی ارسال کنید.")
        return INTERVIEW

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مصاحبه لغو شد.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ORG_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_org)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_position)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
            INTRO_DONE: [MessageHandler(filters.Regex("^شروع مصاحبه$"), intro_done)],
            INTERVIEW: [MessageHandler(filters.VOICE | filters.AUDIO, collect_audio)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()
