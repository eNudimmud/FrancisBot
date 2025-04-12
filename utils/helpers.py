import json
import aiohttp
import os
from datetime import datetime  # Ajouté ici

async def fetch_price(coin_id):
    """Récupère le prix d’une crypto depuis CoinGecko."""
    from config.settings import COINGECKO_API
    try:
        async with aiohttp.ClientSession() as session:
            url = COINGECKO_API.format(coin_id.lower())
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get(coin_id.lower(), {}).get("usd")
    except Exception as e:
        print(f"🚜 Erreur réseau : {e}")
        return None

def load_json(file_path, default=None):
    """Charge un fichier JSON ou retourne une valeur par défaut."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return default or {}

def save_json(file_path, data):
    """Sauvegarde des données dans un fichier JSON."""
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_portfolio(user_id):
    """Charge ou initialise un portefeuille utilisateur."""
    from config.settings import PORTFOLIO_DIR
    portfolio_file = os.path.join(PORTFOLIO_DIR, f"{user_id}.json")
    portfolio = load_json(portfolio_file, {"coins": {}, "last_prices": {}, "history": []})
    print(f"[{datetime.now()}] {'Création' if not os.path.exists(portfolio_file) else 'Chargement'} portefeuille pour {user_id}")
    return portfolio, portfolio_file
