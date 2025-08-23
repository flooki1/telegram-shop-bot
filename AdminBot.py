import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ---------- تنظیمات ----------
load_dotenv()
ADMIN_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

PRODUCTS_FILE = "products.json"

# ---------- دیتابیس ----------
def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categories": {}}

def save_products(data):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- هندلرها ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ شما ادمین نیستید.")
        return

    keyboard = [
        ["➕ افزودن دسته", "➕ افزودن محصول"],
        ["📦 لیست دسته‌ها"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 سلام ادمین! به منوی مدیریت خوش اومدی.", reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text
    data = load_products()

    if text == "➕ افزودن دسته":
        context.user_data["mode"] = "add_category"
        await update.message.reply_text("📝 نام دسته جدید را وارد کنید:")

    elif text == "➕ افزودن محصول":
        if not data["categories"]:
            await update.message.reply_text("⚠️ اول باید یک دسته بسازی.")
            return
        context.user_data["mode"] = "add_product_category"
        await update.message.reply_text("📂 نام دسته‌ای که می‌خواهید محصول به آن اضافه کنید را وارد کنید:")

    elif text == "📦 لیست دسته‌ها":
        if not data["categories"]:
            await update.message.reply_text("❌ دسته‌ای وجود ندارد.")
            return
        msg = "📦 دسته‌های موجود:\n" + "\n".join([f"- {cat}" for cat in data["categories"].keys()])
        await update.message.reply_text(msg)

    # --- حالت‌های ورودی ---
    elif context.user_data.get("mode") == "add_category":
        category = text.strip()
        if category in data["categories"]:
            await update.message.reply_text("⚠️ این دسته قبلاً وجود دارد.")
        else:
            data["categories"][category] = []
            save_products(data)
            await update.message.reply_text(f"✅ دسته «{category}» اضافه شد.")
        context.user_data["mode"] = None

    elif context.user_data.get("mode") == "add_product_category":
        category = text.strip()
        if category not in data["categories"]:
            await update.message.reply_text("❌ همچین دسته‌ای وجود ندارد.")
            context.user_data["mode"] = None
            return
        context.user_data["selected_category"] = category
        context.user_data["mode"] = "add_product_name"
        await update.message.reply_text("🛒 نام محصول را وارد کنید:")

    elif context.user_data.get("mode") == "add_product_name":
        product_name = text.strip()
        context.user_data["product_name"] = product_name
        context.user_data["mode"] = "add_product_price"
        await update.message.reply_text("💰 قیمت محصول را وارد کنید:")

    elif context.user_data.get("mode") == "add_product_price":
        try:
            price = float(text.strip())
        except ValueError:
            await update.message.reply_text("⚠️ لطفاً یک عدد معتبر وارد کنید.")
            return

        category = context.user_data["selected_category"]
        product_name = context.user_data["product_name"]

        data["categories"][category].append({
            "name": product_name,
            "price": price
        })
        save_products(data)

        await update.message.reply_text(f"✅ محصول «{product_name}» با قیمت {price} اضافه شد.")
        context.user_data.clear()

# ---------- ران ----------
def main():
    app = Application.builder().token(ADMIN_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Admin bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
