import os
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# بارگذاری env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# فایل محصولات
PRODUCTS_FILE = "products.json"

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"پوشاک": [], "محصولات الکترونیکی": []}

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍 محصولات", "📞 ارتباط با ما"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 خوش آمدید به فروشگاه ما", reply_markup=reply_markup)

# مدیریت پیام‌ها
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    products = load_products()

    if text == "🛍 محصولات":
        categories = list(products.keys())
        keyboard = [[cat] for cat in categories]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📂 دسته‌بندی محصولات:", reply_markup=reply_markup)

    elif text in products:
        if products[text]:
            msg = "\n".join([f"🔹 {p}" for p in products[text]])
        else:
            msg = "❌ محصولی در این دسته وجود ندارد."
        await update.message.reply_text(msg)

    elif text == "📞 ارتباط با ما":
        await update.message.reply_text("📩 برای ارتباط با پشتیبانی پیام دهید.")

    else:
        await update.message.reply_text("❓ دستور نامشخص است.")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # 🚀 اجرا روی Render با Webhook
    PORT = int(os.environ.get("PORT", "8443"))
    APP_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    await app.start()
    await app.bot.set_webhook(APP_URL)
    await app.updater.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
