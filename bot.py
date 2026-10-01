import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "📢 Join Chart Pro",
            url="https://t.me/ChartPro"
        )
    ]]

    await update.message.reply_text(
        "👋 Welcome to CHART PRO 📊📈\n\n"
        "Hello Trader! 🚀\n"
        "Chart Pro Official Bot me aapka swagat hai.\n\n"
        "📈 Market & Chart Updates\n"
        "💹 NIFTY • BANK NIFTY • SENSEX\n"
        "🪙 Gold & Forex Updates\n"
        "📚 Trading & Market Learning\n\n"
        "👇 Official Channel Join Karein\n"
        "🔔 Join karke notifications ON kar lein.\n\n"
        "⚠️ Educational purposes only. Trading involves risk.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
