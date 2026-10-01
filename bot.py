import os
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Chart Pro", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify Join", callback_data="verify")]
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


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=query.from_user.id
        )

        if member.status in ["member", "administrator", "creator"]:
            menu = [
                [
                    InlineKeyboardButton("📊 Market Updates", callback_data="market"),
                    InlineKeyboardButton("📈 NIFTY", callback_data="nifty")
                ],
                [
                    InlineKeyboardButton("🪙 Gold & Forex", callback_data="gold"),
                    InlineKeyboardButton("📚 Learning", callback_data="learning")
                ],
                [InlineKeyboardButton("📢 Open Chart Pro", url=CHANNEL_LINK)]
            ]

            await query.message.reply_text(
                "✅ Verification Successful!\n\n"
                "🎉 Welcome to Chart Pro!\n"
                "👇 Ab option select karein:",
                reply_markup=InlineKeyboardMarkup(menu)
            )
        else:
            await query.message.reply_text(
                "❌ Pehle Chart Pro channel join karein.\n"
                "Uske baad ✅ Verify Join dabayein."
            )

    except Exception:
        await query.message.reply_text(
            "❌ Verification nahi ho paya.\n"
            "Bot ko channel me Admin rakhein aur dobara try karein."
        )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "market": "📊 MARKET UPDATES\n\nNIFTY • BANK NIFTY • SENSEX market updates.",
        "nifty": "📈 NIFTY\n\nNIFTY & BANK NIFTY chart-based educational updates.",
        "gold": "🪙 GOLD & FOREX\n\nGold & Forex market educational updates.",
        "learning": "📚 MARKET LEARNING\n\nCharts, trading education & risk management.\n\n⚠️ Trading involves risk."
    }

    await query.message.reply_text(messages[query.data])


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
app.add_handler(
    CallbackQueryHandler(
        menu,
        pattern="^(market|nifty|gold|learning)$"
    )
)

app.run_polling()
