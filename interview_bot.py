import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          ContextTypes, ConversationHandler, filters)

# مراحل گفتگو
(START, NAME, ORGANIZATION, POSITION, EXPERIENCE, INTERVIEW) = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[KeyboardButton("تکمیل اطلاعات")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        """
این ربات با هدف بررسی نقش روابط عمومی شهرداری قزوین در هویت‌سازی فرهنگی از طریق اجلاس بین‌المللی شهرداران جاده ابریشم طراحی شده است.

مشارکت شما در پاسخ به این مصاحبه، در مسیر توسعه برنامه‌های فرهنگی آینده کمک شایانی خواهد کرد.
        """,
        reply_markup=reply_markup
    )
    return START

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("نام و نام خانوادگی:")
    return NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("ارگان محل خدمت: \n☐ دولتی\t☐ خصوصی")
    return ORGANIZATION

async def handle_organization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['organization'] = update.message.text
    await update.message.reply_text("جایگاه سازمانی: \n☐ کارشناس \t☐ مدیر میانی ☐ مدیر ارشد")
    return POSITION

async def handle_position(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['position'] = update.message.text
    await update.message.reply_text("سابقه فعالیت در حوزه روابط عمومی دارد: ☐ بله ☐ خیر")
    return EXPERIENCE

async def handle_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['experience'] = update.message.text
    await update.message.reply_text(
        "با انجام این مصاحبه، گامی موثر در مسیر هويت سازي (برندسازي) فرهنگ شهري قزوین برمی‌دارید.\n"
        "راهنما: با ظاهر شدن سوال، شما می‌توانید صدای خود را در پاسخ به سوال ضبط و ارسال کنید."
    )
    keyboard = [[KeyboardButton("شروع مصاحبه")]]
    await update.message.reply_text("برای شروع مصاحبه، دکمه زیر را فشار دهید.",
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return INTERVIEW

questions = [
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

async def handle_interview(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['question_index'] = 0
    await update.message.reply_text(questions[0])
    return INTERVIEW

async def handle_voice_or_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    index = context.user_data.get('question_index', 0)
    user_id = update.effective_user.id
    name = context.user_data.get('name', 'بدون نام')

    # ارسال پیام به آیدی مشخص‌شده
    admin_id = "rezakhooban"
    msg_text = f"👤 {name}\n\nپاسخ سوال {index+1}:"

    if update.message.voice:
        await context.bot.send_voice(chat_id=f"@{admin_id}", voice=update.message.voice.file_id, caption=msg_text)
    elif update.message.text:
        await context.bot.send_message(chat_id=f"@{admin_id}", text=f"{msg_text}\n{update.message.text}")

    index += 1
    if index < len(questions):
        context.user_data['question_index'] = index
        await update.message.reply_text(questions[index])
        return INTERVIEW
    else:
        await update.message.reply_text("✅ مصاحبه به پایان رسید. از مشارکت شما سپاسگزاریم.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("مصاحبه لغو شد.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(os.getenv("TOKEN", "8209512056:AAEfFgOISrub-n8KdaoEusAEj7d_55LZCkI")).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(filters.TEXT & filters.Regex("تکمیل اطلاعات"), handle_start_button)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            ORGANIZATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_organization)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_position)],
            EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_experience)],
            INTERVIEW: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("شروع مصاحبه"), handle_voice_or_text),
                MessageHandler(filters.VOICE, handle_voice_or_text),
                MessageHandler(filters.Regex("شروع مصاحبه"), handle_interview)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == '__main__':
    main()
