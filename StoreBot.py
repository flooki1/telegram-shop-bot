import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# بارگذاری فایل .env
load_dotenv()

# گرفتن توکن از Environment Variable
TOKEN = "8402260828:AAHniaeZ_bfNyGe6HCZgHnn0qVPNkWWkaL4"

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN در Environment Variable تنظیم نشده است!")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍️ محصولات", "📞 ارتباط با ما"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("سلام 👋\nخوش آمدید به فروشگاه ما 🛒", reply_markup=reply_markup)

# پیام‌های منو
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🛍️ محصولات":
        categories = "دسته‌بندی محصولات:\n\n👕 پوشاک\n💻 الکترونیکی\n📚 کتاب"
        await update.message.reply_text(categories)

    elif text == "📞 ارتباط با ما":
        await update.message.reply_text("فعلا اطلاعات تماس ثبت نشده است.")

    else:
        await update.message.reply_text("دستور نامعتبر ❌")

# main bot
async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())



