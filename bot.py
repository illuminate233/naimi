
import logging
import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8056412048:AAGGX8NsW5c1DbkpnsmpGYh0XeQdLl0dSs8"
ADMIN_ID = 6956680309
CHANNEL_LINK = "https://t.me/+Zwx3Y0CHp_RmYzEy"

photo_posts = []
video_posts = []
start_clicks = 0

# Клавиатура выбора
def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Photo", callback_data="photo")],
        [InlineKeyboardButton("🎥 Video", callback_data="video")]
    ])

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_clicks
    start_clicks += 1
    with open("start.jpg", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="Hey cutie! Ready to explore something fun and sweet? 💖 Choose what you’d love to see first 👇",
            reply_markup=main_keyboard()
        )

# Обработка кнопок
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "photo" and photo_posts:
        msg_id = random.choice(photo_posts)
        await context.bot.forward_message(chat_id=query.message.chat.id, from_chat_id=ADMIN_ID, message_id=msg_id)
        await query.message.reply_text("Aww~ isn't it lovely? Wanna peek at a video next? 😚", reply_markup=main_keyboard())

    elif query.data == "video" and video_posts:
        msg_id = random.choice(video_posts)
        await context.bot.forward_message(chat_id=query.message.chat.id, from_chat_id=ADMIN_ID, message_id=msg_id)
        await query.message.reply_text(
            f"Hehe, that was just a little teaser 😳\nYou can see the full magic on the channel 👉 {CHANNEL_LINK}\n\nWanna peek at something else? 💕",
            reply_markup=main_keyboard()
        )

# Сохраняем новый контент
async def save_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.video:
        video_posts.append(update.message.message_id)
        await update.message.reply_text("🎞️ Video saved.")
    elif update.message.photo:
        photo_posts.append(update.message.message_id)
        await update.message.reply_text("📸 Photo saved.")

# Статистика
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Access denied.")
        return
    await update.message.reply_text(f"📊 Bot Usage Stats:\nStart clicks: {start_clicks}\nPhotos: {len(photo_posts)}\nVideos: {len(video_posts)}")

# Логгирование
logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(handle_choice))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, save_post))

app.run_polling()
