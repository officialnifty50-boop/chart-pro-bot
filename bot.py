import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]

# Chart Pro channel
CHANNEL_USERNAME = "@ChartPro"
CHANNEL_LINK = "https://t.me/ChartPro"


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
                callback_data="verify_join"
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


async def verify_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.message.reply_text(
                "✅ Verification Successful!\n\n"
                "🎉 Aap Chart Pro channel join kar chuke hain.\n"
                "📊 Welcome to Chart Pro!"
            )
        else:
            await query.answer(
                "❌ Pehle Chart Pro channel join karein.",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "❌ Verification nahi ho paya.\n"
            "Bot ko channel me Admin banana zaroori hai.",
            show_alert=True
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_join, pattern="^verify_join$"))

    print("Chart Pro Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
