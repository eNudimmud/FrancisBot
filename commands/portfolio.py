from telegram import Update
from telegram.ext import ContextTypes
from utils.helpers import load_portfolio, save_json, fetch_price
from config.settings import DAILY_PRICES, DAILY_PRICES_FILE, MILK, MILK_FILE
import random
from datetime import datetime

async def portefeuille(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    portfolio, portfolio_file = load_portfolio(user_id)

    if not context.args:
        await update.message.reply_text(
            "🚜 **Chers amis, bienvenue dans ton champ simulé !** dit Francis, votre serviteur du canton de Vaud. 🌾\n"
            "Ici, tu peux t’entraîner au trading avec des prix réels, sans risquer un sou ! C’est ma ferme numérique pour apprendre et grandir ensemble. Voici comment ça marche :\n\n"
            "✨ **Comment l’utiliser ?**\n"
            "- `/portefeuille ajouter <crypto> <quantité>` : Plante une crypto dans ton champ (ex. `/portefeuille ajouter BTC 0.1`).\n"
            "- `/portefeuille voir` : Regarde ce que tu as cultivé et sa valeur en USD.\n"
            "- `/portefeuille stats` : Vérifie l’évolution de ton champ sur les 5 dernières minutes.\n"
            "- `/portefeuille retirer <crypto> <quantité>` : Récolte une crypto (ex. `/portefeuille retirer ETH 1`).\n"
            "- `/portefeuille top` : Découvre les fermiers les plus prospères.\n\n"
            "🌟 **Pourquoi s’entraîner ici ?**\n"
            "Pas de pertes, juste du plaisir et de l’apprentissage ! Chaque action te rapporte du $MILK fictif, que tu peux stacker en $CHEESE avec `/stack`. Prépare-toi ainsi pour les services premium et les NFT Highland à venir. Cultive ton savoir-faire avec moi avant de te lancer dans le grand marché !\n"
            "Essaie donc, tape une commande ci-dessus et fais pousser tes talents !",
            parse_mode="Markdown"
        )
        return

    action = context.args[0].lower()

    if action == "ajouter":
        if len(context.args) < 3:
            await update.message.reply_text("🚜 Usage : /portefeuille ajouter <crypto> <quantité>")
            return
        coin, amount = context.args[1].upper(), float(context.args[2])
        if amount <= 0:
            await update.message.reply_text("❌ Quantité positive requise !")
            return

        price = DAILY_PRICES["prices"].get(coin, 0) or await fetch_price(coin)
        if not price:
            await update.message.reply_text(f"❌ {coin} introuvable ou erreur marché !")
            return

        portfolio["coins"][coin] = portfolio["coins"].get(coin, 0) + amount
        portfolio["last_prices"][coin] = price
        portfolio["history"].append({"action": "buy", "coin": coin, "amount": amount, "price": price, "timestamp": datetime.now().isoformat()})
        save_json(portfolio_file, portfolio)
        DAILY_PRICES["prices"][coin] = price
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)

        milk_gain = random.randint(1, 5)
        MILK[user_id] = MILK.get(user_id, 0) + milk_gain
        save_json(MILK_FILE, MILK)

        await update.message.reply_text(f"🌾 {amount} {coin} planté ! Prix : ${price}\n+{milk_gain} $MILK – futurs boosts avec NFT Highland !")

    elif action == "voir":
        if not portfolio["coins"]:
            await update.message.reply_text("🚜 Ton champ est vide !")
            return
        total_value, message = 0, "📊 Ton champ :\n"
        for coin, amount in portfolio["coins"].items():
            price = DAILY_PRICES["prices"].get(coin, 0) or await fetch_price(coin)
            if price:
                DAILY_PRICES["prices"][coin] = price
                value = amount * price
                total_value += value
                message += f"{coin}: {amount} (${value:.2f} USD)\n"
            else:
                message += f"{coin}: {amount} (prix indisponible)\n"
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)
        message += f"**Valeur totale** : ${total_value:.2f} USD"
        await update.message.reply_text(message, parse_mode="Markdown")

    elif action == "stats":
        if not portfolio["coins"]:
            await update.message.reply_text("🚜 Ton champ est vide !")
            return
        total_change, message = 0, "📈 Évolution (5 min) :\n"
        for coin, amount in portfolio["coins"].items():
            old_price = portfolio["last_prices"].get(coin, 0)
            new_price = DAILY_PRICES["prices"].get(coin, 0) or await fetch_price(coin)
            if not new_price:
                message += f"{coin}: Prix indisponible\n"
                continue
            if old_price == 0:
                old_price = new_price
                portfolio["last_prices"][coin] = new_price
                message += f"{coin}: Initialisation en cours\n"
                continue
            previous_price = DAILY_PRICES["previous_prices"].get(coin, old_price)
            if previous_price == 0:
                message += f"{coin}: Pas de données historiques\n"
                continue
            change = ((new_price - previous_price) / previous_price) * 100
            value_change = amount * (new_price - previous_price)
            total_change += value_change
            message += f"{coin}: {change:+.2f}% (${value_change:+.2f} USD)\n"
        save_json(portfolio_file, portfolio)
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)
        message += f"**Changement total** : ${total_change:+.2f} USD"
        await update.message.reply_text(message, parse_mode="Markdown")

    elif action == "retirer":
        if len(context.args) < 3:
            await update.message.reply_text("🚜 Usage : /portefeuille retirer <crypto> <quantité>")
            return
        coin, amount = context.args[1].upper(), float(context.args[2])
        if amount <= 0 or coin not in portfolio["coins"] or portfolio["coins"][coin] < amount:
            await update.message.reply_text(f"❌ Quantité invalide ou pas assez de {coin} !")
            return

        price = DAILY_PRICES["prices"].get(coin, 0) or await fetch_price(coin)
        if not price:
            await update.message.reply_text(f"❌ {coin} introuvable ou erreur marché !")
            return

        portfolio["coins"][coin] -= amount
        if portfolio["coins"][coin] <= 0:
            del portfolio["coins"][coin]
        portfolio["last_prices"][coin] = price
        portfolio["history"].append({"action": "sell", "coin": coin, "amount": amount, "price": price, "timestamp": datetime.now().isoformat()})
        save_json(portfolio_file, portfolio)
        DAILY_PRICES["prices"][coin] = price
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)

        milk_gain = random.randint(1, 3)
        MILK[user_id] = MILK.get(user_id, 0) + milk_gain
        save_json(MILK_FILE, MILK)

        await update.message.reply_text(f"🌾 Récolté {amount} {coin} !\n+{milk_gain} $MILK – futurs boosts avec NFT Highland !")

    elif action == "top":
        from config.settings import PORTFOLIO_DIR
        rankings = []
        for filename in os.listdir(PORTFOLIO_DIR):
            if filename.endswith(".json"):
                user_id = filename[:-5]
                portfolio = load_json(os.path.join(PORTFOLIO_DIR, filename))
                initial_value, realized_gains, current_value = 0, 0, 0
                for tx in portfolio.get("history", []):
                    if tx["action"] == "buy":
                        initial_value += tx["amount"] * tx["price"]
                    elif tx["action"] == "sell":
                        buy_txs = [t for t in portfolio["history"] if t["action"] == "buy" and t["coin"] == tx["coin"]]
                        if buy_txs:
                            avg_buy_price = sum(t["amount"] * t["price"] for t in buy_txs) / sum(t["amount"] for t in buy_txs)
                            realized_gains += tx["amount"] * (tx["price"] - avg_buy_price)
                for coin, amount in portfolio.get("coins", {}).items():
                    price = DAILY_PRICES["prices"].get(coin, 0) or await fetch_price(coin)
                    if price:
                        current_value += amount * price
                        DAILY_PRICES["prices"][coin] = price
                percentage_gain = ((current_value + realized_gains - initial_value) / initial_value * 100) if initial_value > 0 else 0
                rankings.append((user_id, percentage_gain))
        save_json(DAILY_PRICES_FILE, DAILY_PRICES)

        if not rankings:
            await update.message.reply_text("🚜 Aucun fermier n’a encore planté !")
            return
        rankings.sort(key=lambda x: x[1], reverse=True)
        message = "🏆 Top fermiers (par % de gain) :\n"
        for i, (user_id, percentage) in enumerate(rankings[:5], 1):
            try:
                user = await context.bot.get_chat(user_id)
                message += f"{i}. @{user.username or user.first_name}: {percentage:+.2f}%\n"
            except:
                message += f"{i}. Fermier #{user_id[:4]}: {percentage:+.2f}%\n"
        await update.message.reply_text(message, parse_mode="Markdown")

    else:
        await update.message.reply_text("🚜 Usage : /portefeuille [ajouter <crypto> <quantité> | voir | stats | retirer <crypto> <quantité> | top]")
