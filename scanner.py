# scanner.py - Core Memecoin Scanning Logic
import requests
import time
import json
from datetime import datetime
import os

# Environment validation
if not os.getenv("TG_TOKEN") or not os.getenv("TG_CHAT_ID"):
    raise ValueError("Missing Telegram credentials in environment variables")

# Configuration
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"
COINGECKO_API = "https://api.coingecko.com/api/v3"
DEFAULT_PRESET = "Aggressive"

# Presets
PRESETS = {
    "Aggressive": {
        "min_pump": 15,
        "max_mcap": 30e6,
        "max_age": 5,
        "min_liquidity": 2,
        "max_dev_hold": 0.2,
        "min_1h_txs": 150
    },
    "Safe": {
        "min_pump": 25,
        "max_mcap": 10e6,
        "max_age": 15,
        "min_liquidity": 5,
        "max_dev_hold": 0.1,
        "min_1h_txs": 300
    }
}
        
def fetch_dex_pairs(chain="solana"):
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{chain}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get("pairs") or []  # Force empty list if None
        return []
    except Exception as e:
        print(f"⚠️ DEX Error: {e}")
        return []
    
        

def filter_coins(pairs, preset_name="Aggressive"):
    if not isinstance(pairs, list):  # Critical check
        print(f"⚠️ Invalid pairs data: {type(pairs)}")
        return []
    """Apply preset filters to coin list"""
    preset = PRESETS.get(preset_name, PRESETS[DEFAULT_PRESET])
    return [
        p for p in pairs if (
            p["price_change"] >= preset["min_pump"] and
            p["liquidity"] >= preset["min_liquidity"] and
            p["dev_hold"] <= preset["max_dev_hold"] and
            p["age_min"] <= preset["max_age"]
        )
    ]

def format_results(coins):
    """Convert coin data to readable text"""
    return "\n".join(
        f"{c['symbol']} | {c['price_change']:.1f}% | MC: ${c['liquidity']/1e6:.1f}M"
        for c in coins[:10]  # Top 10 results
    )
