# automation.py - Fixed Version
import os
import asyncio
import time
from scanner import fetch_dex_pairs, filter_coins, format_results
from telegram import Bot
from telegram.error import TelegramError

DEBUG = True

async def send_alert(text):
    try:
        bot = Bot(token=os.getenv("TG_TOKEN"))
        await bot.send_message(
            chat_id=os.getenv("TG_CHAT_ID"),
            text=text[:4000]
        )
    except TelegramError as e:
        print(f"Telegram error: {e}")

async def automated_scan():
    try:
        print("🔄 Starting scan...")
        pairs = fetch_dex_pairs()
        print(f"📊 Fetched {len(pairs)} pairs")
        
        filtered = filter_coins(pairs)
        print(f"✅ Filtered to {len(filtered)} coins")
        
        if filtered:
            await send_alert(f"🔄 Results:\n{format_results(filtered)}")
        else:
            await send_alert("⚠️ No coins matched filters")
            
    except Exception as e:
        error_msg = f"🔥 Scan failed: {str(e)[:200]}"
        print(error_msg)
        await send_alert(error_msg)

if __name__ == "__main__":
    asyncio.run(automated_scan())
