import json
import os

# Constantes
CONFIG_FILE = "config.json"
PORTFOLIO_DIR = "portefeuilles"
MILK_FILE = "milk.json"
CHEESE_FILE = "cheese.json"
DAILY_PRICES_FILE = "daily_prices.json"
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"
PRICE_UPDATE_INTERVAL = 300  # 5 minutes

# Chargement config.json
try:
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
    CONSEILS = config["conseils"]
except (FileNotFoundError, KeyError) as e:
    print(f"❌ Erreur config : {e}")
    exit(1)

# Création du dossier portefeuilles si inexistant
if not os.path.exists(PORTFOLIO_DIR):
    os.makedirs(PORTFOLIO_DIR)

# Chargement initial des données
from utils.helpers import load_json
MILK = load_json(MILK_FILE, {})
CHEESE = load_json(CHEESE_FILE, {})
DAILY_PRICES = load_json(DAILY_PRICES_FILE, {"last_update": "", "prices": {}, "previous_prices": {}})
