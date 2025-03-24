from telegram.ext import ContextTypes
from config.settings import DAILY_PRICES, DAILY_PRICES_FILE, PORTFOLIO_DIR, COINGECKO_API
from utils.helpers import load_json, save_json
from datetime import datetime, timedelta
import aiohttp
import os  # Ajouté ici

async def update_five_minutely_prices(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    if not DAILY_PRICES["last_update"] or (datetime.fromisoformat(DAILY_PRICES["last_update"]) < now - timedelta(minutes=5)):
        print(f"[{now}] Mise à jour des prix...")
        DAILY_PRICES["previous_prices"] = DAILY_PRICES["prices"].copy()
        coins = {coin for filename in os.listdir(PORTFOLIO_DIR) if filename.endswith(".json")
                 for coin in load_json(os.path.join(PORTFOLIO_DIR, filename)).get("coins", {}).keys()}
        if coins:
            async with aiohttp.ClientSession() as session:
                url = COINGECKO_API.format(",".join(coin.lower() for coin in coins))
                async with session.get(url) as resp:
                    if resp.status == 200:
                        prices = await resp.json()
                        DAILY_PRICES["last_update"] = now.isoformat()
                        for coin in coins:
                            if coin.lower() in prices:
                                DAILY_PRICES["prices"][coin] = prices[coin.lower()]["usd"]
                        save_json(DAILY_PRICES_FILE, DAILY_PRICES)
                        print(f"[{now}] Prix mis à jour : {DAILY_PRICES['prices']}")
                    else:
                        print(f"[{now}] Erreur CoinGecko : {resp.status}")
