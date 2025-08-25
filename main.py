import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")  # e.g. "instagram-scraper-2022.p.rapidapi.com"

# ---------- Start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Support Channel", url="https://t.me/bye_artist")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_animation(
        animation="https://files.catbox.moe/lhbsqt.mp4",
        caption="👋 <b>Welcome to Reels Downloader Bot!</b>\n\n📌 Just send me an Instagram Reels link.",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ---------- Handle Links ----------
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com/reel" not in url:
        await update.message.reply_text("❌ Please send a valid Instagram Reels link.")
        return

    try:
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }
        params = {"url": url}

        response = requests.get(
            f"https://{RAPIDAPI_HOST}/download",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            video_url = data.get("video", None)

            if video_url:
                await update.message.reply_video(
                    video=video_url,
                    caption="✅ Here is your downloaded reel!"
                )
            else:
                await update.message.reply_text("❌ Could not fetch video. Try again.")

        else:
            await update.message.reply_text("⚠️ API Error: " + str(response.status_code))

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# ---------- Main ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    app.run_polling()

if __name__ == "__main__":
    main()
