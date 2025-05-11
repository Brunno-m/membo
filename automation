# automation.py - Scheduled Scanning
import os
import time
from scanner import fetch_dex_pairs, filter_coins, format_results
from telegram import Bot

def send_alert(text):
    """Send results to Telegram"""
    Bot(token=os.getenv("TG_TOKEN")).send_message(
        chat_id=os.getenv("TG_CHAT_ID"),
        text=text
    )

def automated_scan():
    """Run scan with default preset"""
    pairs = fetch_dex_pairs()
    filtered = filter_coins(pairs)  # Uses DEFAULT_PRESET
    if filtered:
        send_alert(f"🔄 Auto-Scan Results:\n{format_results(filtered)}")
    else:
        send_alert("⚠️ No coins matching criteria")

if __name__ == "__main__":
    while True:
        automated_scan()
        time.sleep(10800)  # 3 hours
