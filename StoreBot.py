import os
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
def start(update: Update, context: CallbackContext):
    keyboard = [["🛍 محصولات", "📞 ارتباط با ما"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("👋 خوش آمدید به فروشگاه ما", reply_markup=reply_markup)

# مدیریت پیام‌ها
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    products = load_products()

    if text == "🛍 محصولات":
        categories = list(products.keys())
        keyboard = [[cat] for cat in categories]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("📂 دسته‌بندی محصولات:", reply_markup=reply_markup)

    elif text in products:
        if products[text]:
            msg = "\n".join([f"🔹 {p}" for p in products[text]])
        else:
            msg = "❌ محصولی در این دسته وجود ندارد."
        update.message.reply_text(msg)

    elif text == "📞 ارتباط با ما":
        update.message.reply_text("📩 برای ارتباط با پشتیبانی پیام دهید.")

    else:
        update.message.reply_text("❓ دستور نامشخص است.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # ------------------------------
    # 🚀 اجرا روی Render با Webhook
    # ------------------------------
    PORT = int(os.environ.get("PORT", "8443"))
    APP_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=APP_URL
    )

    updater.idle()

if __name__ == "__main__":
    main()

