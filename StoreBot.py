from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 توکن ربات (اینجا توکن خودتو بذار)
TOKEN = "8402260828:AAHniaeZ_bfNyGe6HCZgHnn0qVPNkWWkaL4"

# ✅ دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 به فروشگاه خوش اومدی!")

# ✅ دستور /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لیست دستورات:\n/start - شروع\n/help - راهنما")

# ✅ پیام عادی (اکو)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"شما گفتید: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()

    # هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot is running...")
    app.run_polling()   # 🚀 دیگه نیازی به asyncio نداری

if __name__ == "__main__":
    main()
