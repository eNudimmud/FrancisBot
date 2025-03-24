from telegram import Update
from telegram.ext import ContextTypes
import ephem
from utils.helpers import fetch_price, save_json
from config.settings import DAILY_PRICES, DAILY_PRICES_FILE

# Mapping des symboles vers les ID CoinGecko
COIN_IDS = {
    "BTC": "bitcoin",
    "SOL": "solana",
    "ETH": "ethereum",
    "XRP": "ripple",
    "ADA": "cardano",
    # Ajoute d'autres cryptos si besoin
}

async def lune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    moon = ephem.Moon()
    moon.compute()
    phase = moon.phase
    phases = {
        (0, 7.4): "🌑 Nouvelle Lune : Bon moment pour initier des projets, mais attention à l’incertitude !",
        (7.4, 14.8): "🌓 Premier Quartier : Énergie croissante, bonne période pour la prise de décisions.",
        (14.8, 22.1): "🌕 Pleine Lune : Forte émotion et volatilité sur le marché, prudence !",
        (22.1, 100): "🌗 Dernier Quartier : Période de réflexion, bon moment pour sécuriser ses profits."
    }
    for (min_phase, max_phase), msg in phases.items():
        if min_phase <= phase < max_phase:
            await update.message.reply_text(msg, parse_mode="Markdown")
            break

async def swissmilk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🥛 **Francis prépare sa récolte de $MILK !** 🚀\n\n"
        "Bientôt, tu pourras accéder à des services avancés de trading grâce à $MILK.\n"
        "🔥 **Reste attentif !** $MILK arrive bientôt...",
        parse_mode="Markdown"
    )

async def prix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🚜 Usage : /prix <symbole> (ex. /prix BTC)")
        return
    coin = context.args[0].upper()
    # Convertir le symbole en ID CoinGecko
    coin_id = COIN_IDS.get(coin, coin.lower())  # Si pas dans COIN_IDS, tente en minuscule
    price = DAILY_PRICES["prices"].get(coin, 0) if coin in DAILY_PRICES["prices"] else await fetch_price(coin_id)
    if price:
        DAILY_PRICES["prices"][coin] = price
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)
        await update.message.reply_text(f"🌾 Le prix de {coin} est de ${price} USD !")
    else:
        await update.message.reply_text(f"❌ {coin} introuvable ou erreur marché, vérifie le symbole !")
