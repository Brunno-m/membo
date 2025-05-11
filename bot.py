import json, requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Load presets
presets = {
    'Aggressive': {'min_pump': 15, 'max_mcap': 30e6},
    'Safe': {'min_pump': 25, 'max_mcap': 10e6}
}

DEFAULT_PRESET = 'Aggressive'  # Set default here

# Scanner Core (replace with your functions)
def scan_coins(settings):
    api_url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    data = requests.get(api_url).json()
    return [c for c in data['pairs'] if (
        c['priceChange']['h24'] >= settings['min_pump'] and
        c['fdv'] <= settings['max_mcap']
    )]

# Telegram UI
async def start(update: Update, _):
    keyboard = [
        [InlineKeyboardButton(n, callback_data=f"preset_{n}") for n in presets]
    ]
    await update.message.reply_text(
        "Choose strategy:",
        reply_markup=InlineKeyboardMarkup(keyboard)
)

async def button_click(update: Update, _):
    preset = update.callback_query.data.split('_')[1]
    results = scan_coins(presets[preset])
    await update.callback_query.edit_message_text(f"✅ {preset}:\n{results[:2]}...")

# Automated Scan
def automated_scan():
    results = scan_coins(presets[DEFAULT_PRESET])
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
        'chat_id': CHAT_ID,
        'text': f"🔄 Auto-scanned:\n{results[:5]}"
    })

if __name__ == "__main__":
    app = Application.builder().token("TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()
