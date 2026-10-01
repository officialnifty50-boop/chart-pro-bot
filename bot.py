import os
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]

CHANNEL_USERNAME = "@ChartPro"
CHANNEL_LINK = "https://t.me/ChartPro"

IST = ZoneInfo("Asia/Kolkata")


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Join Chart Pro",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Verify Join",
                callback_data="verify"
            )
        ]
    ]

    await update.message.reply_text(
        "👋 Welcome to CHART PRO 📊\n\n"
        "Hello Trader! 🚀\n"
        "Chart Pro Official Bot me aapka swagat hai.\n\n"
        "📈 Market & Chart Updates\n"
        "💹 NIFTY • BANK NIFTY • SENSEX\n"
        "🪙 Gold & Forex Updates\n"
        "📚 Trading & Market Learning\n\n"
        "👇 Pehle Official Channel Join karein.\n"
        "Join karne ke baad ✅ Verify Join dabayein.\n\n"
        "⚠️ Educational purposes only. Trading involves risk.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------- VERIFY ----------
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:
            await query.message.reply_text(
                "✅ Verification Successful!\n\n"
                "🎉 Aap Chart Pro channel join kar chuke hain.\n"
                "📊 Welcome to Chart Pro!"
            )
        else:
            await query.message.reply_text(
                "❌ Channel join nahi hua.\n\n"
                "Pehle 📢 Join Chart Pro button se channel join karein,\n"
                "phir ✅ Verify Join dabayein."
            )

    except Exception as e:
        print("Verification error:", e)

        await query.message.reply_text(
            "⚠️ Verification nahi ho paya.\n"
            "Channel join karke dobara Verify dabayein."
        )


# ---------- 9 AM POST ----------
async def morning_post(context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🌅 GOOD MORNING CHART PRO FAMILY 📊\n\n"
        "📈 Today's Market Watch\n\n"
        "💹 NIFTY 50\n"
        "📊 BANK NIFTY\n"
        "📉 SENSEX\n"
        "🪙 GOLD\n"
        "💱 FOREX\n\n"
        "🔔 Aaj ke market updates ke liye notifications ON rakhein.\n\n"
        "📚 Educational purposes only.\n"
        "⚠️ Trading involves risk."
    )

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=text
    )


# ---------- 1 PM POST ----------
async def afternoon_post(context: ContextTypes.DEFAULT_TYPE):

    text = (
        "📊 CHART PRO — MARKET UPDATE\n\n"
        "🕐 Afternoon Market Check\n\n"
        "📈 NIFTY 50\n"
        "💹 BANK NIFTY\n"
        "📉 SENSEX\n"
        "🪙 GOLD & FOREX\n\n"
        "🔔 Market updates ke liye Chart Pro ke saath jude rahein.\n\n"
        "⚠️ Educational purposes only. Trading involves risk."
    )

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=text
    )


# ---------- 6 PM POST ----------
async def evening_post(context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🌆 CHART PRO EVENING UPDATE 📊\n\n"
        "📈 Today's Market Wrap\n\n"
        "💹 NIFTY • BANK NIFTY • SENSEX\n"
        "🪙 Gold & Forex\n"
        "📚 Market Learning\n\n"
        "🔔 Kal ke updates ke liye notifications ON rakhein.\n\n"
        "⚠️ Educational purposes only. Trading involves risk."
    )

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=text
    )


# ---------- BOT ----------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))


# ---------- AUTO POST SCHEDULE ----------
job_queue = app.job_queue

job_queue.run_daily(
    morning_post,
    time=time(hour=9, minute=0, tzinfo=IST)
)

job_queue.run_daily(
    afternoon_post,
    time=time(hour=13, minute=0, tzinfo=IST)
)

job_queue.run_daily(
    evening_post,
    time=time(hour=18, minute=0, tzinfo=IST)
)


print("Chart Pro Bot Running...")
app.run_polling()
