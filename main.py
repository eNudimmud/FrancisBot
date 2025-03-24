import asyncio
import nest_asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import TELEGRAM_BOT_TOKEN
from commands.basic import start, help_command, interactivity
from commands.advice import trading, degen, risques, scam, bots, conseil
from commands.info import lune, swissmilk, prix
from commands.portfolio import portefeuille
from commands.token import milk, stack, nft
from tasks.price_update import update_five_minutely_prices

# Permet de gérer plusieurs boucles d'événements dans Termux
nest_asyncio.apply()

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    commands = [
        ("start", start), ("help", help_command), ("trading", trading),
        ("degen", degen), ("risques", risques), ("scam", scam),
        ("bots", bots), ("conseil", conseil), ("lune", lune),
        ("swissmilk", swissmilk), ("prix", prix), ("portefeuille", portefeuille),
        ("milk", milk), ("stack", stack), ("nft", nft)
    ]
    # Ajouter les CommandHandler pour chaque commande
    for cmd, handler in commands:
        app.add_handler(CommandHandler(cmd, handler))
    # Ajouter le handler pour les messages texte
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interactivity))
    # Ajouter la tâche périodique
    app.job_queue.run_repeating(update_five_minutely_prices, interval=300)
    print("✅ Francis est actif !")
    # Lancer le bot avec polling
    app.run_polling()

if __name__ == "__main__":
    main()
