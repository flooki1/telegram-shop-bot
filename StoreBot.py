import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ---------- تنظیمات ----------
load_dotenv()
STORE_TOKEN = os.getenv("STORE_BOT_TOKEN")  # توکن ربات فروشگاه

PRODUCTS_FILE = "products.json"

# ---------- دیتابیس ----------
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": {}}

# ---------- هندلرها ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛍 محصولات", "📞 ارتباط با ما"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 خوش آمدید به فروشگاه ما!", reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    data = load_products()

    if text == "🛍 محصولات":
        if not data["categories"]:
            await update.message.reply_text("❌ هنوز هیچ محصولی موجود نیست.")
            return
        keyboard = [[cat] for cat in data["categories"].keys()]
        keyboard.append(["⬅️ بازگشت"])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📦 دسته‌های محصولات:", reply_markup=reply_markup)

    elif text in data["categories"].keys():
        products = data["categories"][text]
        if not products:
            await update.message.reply_text("❌ محصولی در این دسته وجود ندارد.")
            return
        msg = f"🛍 محصولات دسته «{text}»:\n"
        for p in products:
            msg += f"- {p['name']} | 💰 {p['price']}\n"
        await update.message.reply_text(msg)

    elif text == "📞 ارتباط با ما":
        await update.message.reply_text("📞 برای ارتباط با ما پیام دهید به: example@example.com")

    elif text == "⬅️ بازگشت":
        keyboard = [["🛍 محصولات", "📞 ارتباط با ما"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("منوی اصلی:", reply_markup=reply_markup)

# ---------- ران ----------
def main():
    app = Application.builder().token(STORE_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🛒 Store bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
