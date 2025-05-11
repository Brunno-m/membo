# bot.py - Telegram Interface
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from scanner import fetch_dex_pairs, filter_coins, format_results, PRESETS

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load from environment (set in GitHub Secrets)
TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

async def start(update: Update, context):
    """Send preset selection menu"""
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"preset_{name}")]
        for name in PRESETS
    ]
    await update.message.reply_text(
        "🔍 Select scanning strategy:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_preset(update: Update, context):
    """Process preset selection"""
    query = update.callback_query
    preset_name = query.data.split("_")[1]
    
    # Fetch and filter coins
    pairs = fetch_dex_pairs()
    filtered = filter_coins(pairs, preset_name)
    
    # Send results
    await query.edit_message_text(
        f"✅ {preset_name} Strategy:\n"
        f"{format_results(filtered)}"
    )

def run_bot():
    """Start the Telegram bot"""
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_preset))
    
    # Start polling
    app.run_polling()

if __name__ == "__main__":
    run_bot()
