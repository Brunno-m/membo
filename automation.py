# automation.py - Optimized with all checks
import os
import time
import requests
from scanner import fetch_dex_pairs, filter_coins, format_results
from telegram import Bot

# Debugging setup
DEBUG = True  # Set to False in production

def log(message):
    if DEBUG:
        print(f"[{time.ctime()}] {message}")

def send_alert(text):
    try:
        Bot(token=os.getenv("TG_TOKEN")).send_message(
            chat_id=os.getenv("TG_CHAT_ID"),
            text=text[:4000]  # Truncate long messages
        )
    except Exception as e:
        log(f"Telegram error: {e}")

def automated_scan():
    try:
        log("🔄 Starting scan...")
        
        # Fetch with rate limit protection
        pairs = fetch_dex_pairs()
        time.sleep(1)  # Avoid API throttling
        log(f"📊 Fetched {len(pairs)} pairs")
        
        # Filter and validate
        filtered = filter_coins(pairs)
        log(f"✅ Filtered to {len(filtered)} coins")
        
        if filtered:
            send_alert(f"🔄 Results:\n{format_results(filtered)}")
        else:
            send_alert("⚠️ No coins matched filters")
            
    except Exception as e:
        error_msg = f"🔥 Scan failed: {str(e)[:200]}"
        log(error_msg)
        send_alert(error_msg)

if __name__ == "__main__":
    automated_scan()
    # For GH Actions, add:
    # while True:
    #     automated_scan()
    #     time.sleep(10800)  # 3 hours
