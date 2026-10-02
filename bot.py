import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==========================================
# SETTINGS
# ==========================================

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Private Chart Pro Telegram Channel
CHANNEL_LINK = "https://t.me/+f05Fzq_lvMk5ZjBl"


# ==========================================
# RENDER FREE WEB SERVER
# ==========================================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Chart Pro Bot is running")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()


# ==========================================
# /START AUTOMATIC MESSAGE
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    first_name = user.first_name or "Trader"

    message = f"""
👋 Welcome {first_name}!

📊 CHART PRO

Welcome to the Chart Pro community.

📈 Market Updates
📊 Chart Learning
📰 Important Market Information
🎯 Trading Education
⏰ Regular Updates

👇 Join our private Telegram channel to continue.

⚠️ Educational content only.
Trading involves market risk.
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 JOIN CHART PRO",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ I HAVE JOINED",
                callback_data="joined"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ ABOUT CHART PRO",
                callback_data="about"
            )
        ]
    ]

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# BUTTON RESPONSES
# ==========================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "joined":

        await query.message.reply_text(
            """✅ Thank you!

Welcome to Chart Pro 📊

You can now follow the private channel for regular updates.

📈 Learn • Understand • Improve

⚠️ No guaranteed profits.
Always manage your own risk."""
        )

    elif query.data == "about":

        await query.message.reply_text(
            """📊 CHART PRO

Chart Pro provides educational market content and regular updates.

📈 Charts
📚 Market Learning
📰 Market Updates
📊 Trading Education

Use the button below to join our private community.""",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📢 JOIN PRIVATE CHANNEL",
                        url=CHANNEL_LINK
                    )
                ]
            ])
        )


# ==========================================
# BOT
# ==========================================

def main():

    # Start HTTP server required by Render Web Service
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Chart Pro Bot Running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
