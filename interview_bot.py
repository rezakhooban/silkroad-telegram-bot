import json
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          CallbackQueryHandler, ConversationHandler, ContextTypes, filters)

START, FULLNAME, ORGAN, POSITION, EXPERIENCE, START_INTERVIEW, QUESTION = range(7)

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

user_data = {}
SAVE_DIR = Path("interview_data")
VOICE_DIR = SAVE_DIR / "voices"
SAVE_DIR.mkdir(exist_ok=True)
VOICE_DIR.mkdir(exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی از طریق اجلاس بین‌المللی شهرداران جاده ابریشم طراحی شده است.
مشارکت شما در پاسخ به این مصاحبه، در مسیر توسعه برنامه‌های فرهنگی آینده کمک شایانی خواهد کرد.
        """,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تکمیل اطلاعات", callback_data="start_info")]])
    )
    return START

async def start_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("نام و نام خانوادگی:", reply_markup=ReplyKeyboardRemove())
    return FULLNAME

async def get_fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {'fullname': update.message.text, 'answers': []}
    buttons = [[
        InlineKeyboardButton("دولتی", callback_data="دولتی"),
        InlineKeyboardButton("خصوصی", callback_data="خصوصی")
    ]]
    await update.message.reply_text("ارگان محل خدمت:", reply_markup=InlineKeyboardMarkup(buttons))
    return ORGAN

async def get_organ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['organ'] = update.callback_query.data
    await update.callback_query.answer()
    buttons = [[
        InlineKeyboardButton("کارشناس", callback_data="کارشناس"),
        InlineKeyboardButton("مدیر میانی", callback_data="مدیر میانی"),
        InlineKeyboardButton("مدیر ارشد", callback_data="مدیر ارشد")
    ]]
    await update.callback_query.message.reply_text("جایگاه سازمانی:", reply_markup=InlineKeyboardMarkup(buttons))
    return POSITION

async def get_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['position'] = update.callback_query.data
    await update.callback_query.answer()
    buttons = [[
        InlineKeyboardButton("بله", callback_data="بله"),
        InlineKeyboardButton("خیر", callback_data="خیر")
    ]]
    await update.callback_query.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد:", reply_markup=InlineKeyboardMarkup(buttons))
    return EXPERIENCE

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id]['experience'] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        """
با انجام این مصاحبه، گامی موثر در مسیر هويت سازي (برندسازي) فرهنگ شهري قزوین برمی دارید.
راهنما: با ظاهر شدن سوال شما می توانید صدای خود را در پاسخ به سوال ضبط و ارسال کنید.
        """,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("شروع مصاحبه", callback_data="begin")]])
    )
    return START_INTERVIEW

async def start_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    context.user_data['q_index'] = 0
    await update.callback_query.message.reply_text(f"سوال 1:\n{QUESTIONS[0]}")
    return QUESTION

async def collect_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_idx = context.user_data.get('q_index', 0)
    uid = update.effective_user.id
    q_text = QUESTIONS[q_idx]
    fullname = user_data.get(uid, {}).get('fullname', f"User_{uid}")

    if update.message.voice:
        file_id = update.message.voice.file_id
        voice_file = await context.bot.get_file(file_id)
        filename = VOICE_DIR / f"{fullname.replace(' ', '_')}_q{q_idx+1}_{uid}.ogg"
        await voice_file.download_to_drive(str(filename))

        user_data[uid]['answers'].append({
            'question': q_text,
            'voice_file_id': file_id,
            'voice_path': str(filename)
        })
        await update.message.forward(chat_id="@rezakhooban")
        await update.message.reply_text("پاسخ صوتی شما دریافت شد. متشکرم ✅")

    q_idx += 1
    if q_idx < len(QUESTIONS):
        context.user_data['q_index'] = q_idx
        await update.message.reply_text(f"سوال {q_idx+1}:\n{QUESTIONS[q_idx]}")
        return QUESTION
    else:
        save_path = SAVE_DIR / f"{fullname.replace(' ', '_')}_{uid}.json"
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(user_data[uid], f, ensure_ascii=False, indent=2)

        await update.message.reply_text("از مشارکت شما سپاسگزاریم. 🎤")
        return ConversationHandler.END

application = ApplicationBuilder().token("8209512056:AAEfFgOISrub-n8KdaoEusAEj7d_55LZCkI").build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [CallbackQueryHandler(start_info, pattern="start_info")],
        FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_fullname)],
        ORGAN: [CallbackQueryHandler(get_organ)],
        POSITION: [CallbackQueryHandler(get_position)],
        EXPERIENCE: [CallbackQueryHandler(get_experience)],
        START_INTERVIEW: [CallbackQueryHandler(start_interview, pattern="begin")],
        QUESTION: [MessageHandler(filters.VOICE, collect_answer)],
    },
    fallbacks=[]
)

application.add_handler(conv_handler)

if __name__ == '__main__':
    application.run_polling()