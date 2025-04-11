
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

OWNER_ID = 6956680309
CHANNEL_LINK = "https://t.me/+Zwx3Y0CHp_RmYzEy"

photo_messages = []
video_messages = []
stats = {"start": 0}

photo_captions = [
    "Here's a lovely moment 🌸 — but wait till you see the video! 🎥",
    "This pic is cute, but videos? They’re next level 😍 Tap that button!",
    "A picture says a lot, but a video... well, it shows everything 😉"
]

video_captions = [
    "Wish I could send the full video here... but Telegram has limits! 😢",
    "This is just a teaser — the full content is waiting on the channel 👀",
    "Can't fit all the fun here — check out the full thing on our channel! 🎬"
]

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Photo", callback_data="photo")],
        [InlineKeyboardButton("🎞️ Video", callback_data="video")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats["start"] += 1
    await update.message.reply_text(
        "Hey there! Ready to see something adorable and fun? 💖",
        reply_markup=main_keyboard()
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "photo":
        if photo_messages:
            msg_id = random.choice(photo_messages)
            caption = random.choice(photo_captions)
            await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=OWNER_ID, message_id=msg_id, caption=caption)
        else:
            await query.message.reply_text("No photos uploaded yet 😢")
        await query.message.reply_text("What would you like next?", reply_markup=main_keyboard())

    elif query.data == "video":
        if video_messages:
            msg_id = random.choice(video_messages)
            caption = random.choice(video_captions)
            await context.bot.copy_message(chat_id=query.message.chat_id, from_chat_id=OWNER_ID, message_id=msg_id, caption=caption)
        else:
            await query.message.reply_text("No videos uploaded yet 😢")
        await query.message.reply_text(f"Watch more on our channel 👉 {CHANNEL_LINK}")

async def save_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_from_chat and update.message.from_user.id == OWNER_ID:
        msg = update.message
        if msg.video:
            video_messages.append(msg.message_id)
            await msg.reply_text("🎞️ Video saved.")
        elif msg.photo:
            photo_messages.append(msg.message_id)
            await msg.reply_text("📸 Photo saved.")
        else:
            await msg.reply_text("Only photos and videos are supported.")

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == OWNER_ID:
        await update.message.reply_text(
            f"📊 Bot Usage Stats:\nStart button pressed: {stats['start']}"
        )
    else:
        await update.message.reply_text("Sorry, stats are for the bot owner only.")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise ValueError("Missing TOKEN environment variable")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_handler))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.FORWARDED, save_forward))

    app.run_polling()

if __name__ == '__main__':
    main()
