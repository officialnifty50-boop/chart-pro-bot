import asyncio
import os
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Chart Pro channel
CHANNEL_ID = "@ChartPro"
CHANNEL_LINK = "https://t.me/+f05Fzq_lvMk5ZjBl"
INDIA_TZ = ZoneInfo("Asia/Kolkata")

# Automatic message time — India Time
AUTOMATIC_MESSAGES = {
    "08:00": (
        "🌅 Good Morning Chart Pro Family 📊\n\n"
        "Start your day with discipline, patience and proper risk management.\n"
        "📈 Learn • Understand • Improve\n\n"
        "⚠️ Educational content only. No guaranteed profits."
    ),

    "13:00": (
        "☀️ Good Afternoon Chart Pro Family 📊\n\n"
        "Stay calm, follow your plan and avoid emotional trading.\n"
        "✅ Protect capital • Manage risk • Keep learning"
    ),

    "18:00": (
        "🌆 Good Evening Chart Pro Family 📊\n\n"
        "Review today's market and prepare for tomorrow.\n"
        "📚 Consistency is more important than excitement."
    ),

    "21:30": (
        "🌙 Good Night Chart Pro Family 📊\n\n"
        "Rest well and return tomorrow with a clear mind.\n"
        "⚠️ Trade responsibly and manage your own risk."
    ),
}


# Render web server
class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Chart Pro Bot is running")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)

    print(f"Web server running on port {port}")

    server.serve_forever()


def main_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 JOIN CHART PRO CHANNEL",
                    url=CHANNEL_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ I Joined",
                    callback_data="joined"
                ),
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about"
                ),
            ],
        ]
    )


# /start command
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    name = user.first_name if user else "Trader"

    message = (
        f"👋 Welcome {name}!\n\n"
        "📊 CHART PRO\n"
        "Trade • Invest • Grow\n\n"
        "✅ Market learning and important updates\n"
        "✅ Trading discipline\n"
        "✅ Risk-management guidance\n"
        "✅ Daily automatic Chart Pro posts\n\n"
        "Join our official channel using the button below.\n\n"
        "⚠️ Educational content only.\n"
        "No guaranteed profits."
    )

    await update.effective_message.reply_text(
        message,
        reply_markup=main_keyboard()
    )


# Buttons
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "joined":

        await query.message.reply_text(
            "✅ Thank you!\n\n"
            "Welcome to Chart Pro 📊\n\n"
            "You can now follow the channel for market updates.\n\n"
            "📈 Learn • Understand • Improve\n\n"
            "⚠️ No guaranteed profits."
        )

    elif query.data == "about":

        await query.message.reply_text(
            "📊 CHART PRO\n\n"
            "Market education, chart learning and trading updates.\n\n"
            "This bot does not provide guaranteed profit or "
            "personal financial advice."
        )


# Test automatic channel posting
async def testpost(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=(
                "✅ Chart Pro automatic posting test successful! 📊\n\n"
                "Bot official channel se connect ho gaya hai."
            )
        )

        await update.effective_message.reply_text(
            "✅ Test message channel me bhej diya."
        )

    except Exception as error:

        await update.effective_message.reply_text(
            f"❌ Test failed: {error}"
        )


# Daily automatic messages
async def automatic_channel_messages(
    application: Application
):

    last_sent = None

    print("Automatic scheduler started — India Time")

    while True:

        now = datetime.now(INDIA_TZ)

        current_time = now.strftime("%H:%M")

        send_key = f"{now.date()}-{current_time}"

        if (
            current_time in AUTOMATIC_MESSAGES
            and last_sent != send_key
        ):

            try:

                await application.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=AUTOMATIC_MESSAGES[current_time]
                )

                last_sent = send_key

                print(
                    f"Automatic message sent at "
                    f"{current_time} IST"
                )

            except Exception as error:

                print(
                    f"Automatic message failed: {error}"
                )

        await asyncio.sleep(20)


async def post_init(application: Application):

    application.create_task(
        automatic_channel_messages(application)
    )


def main():

    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("testpost", testpost)
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
