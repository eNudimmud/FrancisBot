import asyncio
import json
import random
import nest_asyncio
import ephem
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Évite les conflits d'event loop sous Termux
nest_asyncio.apply()

# Charger les clés API Telegram depuis config.json
with open("config.json") as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]

# 📌 Commande /start - Introduction à Francis
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👨‍🌾 **Bienvenue dans Le Club de Francis !** 🚜\n\n"
        "Francis, fermier du canton de Vaud et expert en crypto, est là pour te guider.\n"
        "Tape /help pour voir toutes les commandes disponibles !"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# 📌 Commande /help - Liste des commandes disponibles
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📜 **Commandes de Francis** 📜\n\n"
        "/start - Démarrer Francis 🚀\n"
        "/trading - Conseil de trading classique 📈\n"
        "/degen - Conseil pour le trading degen 💸\n"
        "/risques - Conseil sur la gestion des risques 🛡️\n"
        "/scam - Prévention des arnaques ⚠️\n"
        "/bots - Découvrir les outils et bots 🤖\n"
        "/conseil - Obtenir un conseil crypto aléatoire 🎲\n"
        "/lune - Voir l'impact de la lune sur le marché 🌙\n"
        "/milk - Découvrir la future tokenisation de Francis 🥛"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# 📌 Réponses interactives dans le Club
async def interactivity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    responses = {
        "bonjour": ["👨‍🌾 Salut l’ami ! Une belle journée pour cultiver du BTC ! 🌾", 
                    "🚜 Bonjour camarade ! Prêt à labourer le marché crypto ?", 
                    "🌞 Bonjour ! La lune est-elle favorable aux trades aujourd’hui ? 🌙"],

        "comment ça va ?": ["👨‍🌾 Toujours au top, entre deux récoltes de profits ! 🚀", 
                            "🐄 Ça va bien, merci ! J’étais en train de surveiller les vaches… et le marché crypto !",
                            "📈 Tant que le marché n’est pas en bear market, tout va bien !"],

        "aurevoir": ["👨‍🌾 À plus tard l’ami ! Que tes récoltes de crypto soient abondantes ! 🌾", 
                     "🚜 Reviens quand tu veux ! Francis est toujours là pour conseiller !", 
                     "📉 Fais attention aux chutes de marché et aux rug pulls !"],

        "salut": ["👨‍🌾 Salut mon gars ! Toujours dans la ferme ou sur les marchés ? 🚀", 
                  "👋 Yo ! Ça trade quoi aujourd’hui ?", 
                  "🌞 Salut ! Une belle journée pour récolter des profits !"],
        
        "oh con francis !": ["😆 Oh con ! T'es là toi ? J'étais en train de surveiller mes cryptos et mes vaches en même temps !",
                              "🚜 Ah mais quel plaisir ! Alors, ça fait pousser des tokens ou toujours en train de labourer du vent ?",
                              "🥖 Ah bah ça, si c’est pas mon trader préféré ! T'as vu le marché ? Ça bouge plus qu’un cassoulet en digestion !",
                              "🍷 Oh peuchère ! T’as flairé un bon airdrop ou tu viens juste prendre un Ricard ?",
                              "🎉 Ahahah ! Mais t’as mis le bon stop-loss au moins ? Parce que sinon, c’est la gadoue mon gars !"],
    }

    for key in responses:
        if key in text:
            await update.message.reply_text(random.choice(responses[key]))
            return

# 📈 Commande /trading - Conseils de trading classique
async def trading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "📈 *HODL* : Acheter et conserver à long terme, comme un bon vin qui se bonifie avec le temps. 🍷",
        "📉 *Scalping* : Trades rapides sur de petites variations de prix, comme traire une vache pour chaque goutte de lait. 🥛",
        "🌾 *Swing Trading* : Exploiter les cycles du marché, comme planter et récolter en fonction des saisons."
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# 🚀 Commande /degen - Conseils pour le trading Degen
async def degen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "⚡ *Surveille les tendances sur X avec LunarCrush et AssetDash* : La hype est ton meilleur indicateur !",
        "🤖 *Utilise un bot comme ToxiSolBot ou Axiom pour exécuter tes ordres automatiquement*.",
        "💥 *Arbitrage entre exchanges* : Si Binance vend moins cher qu’Uniswap, achète ici et vends là-bas !",
        "🛑 *Fixe des stop-loss et take-profits* : Même en mode degen, on ne joue pas sans parachute.",
        "📊 *Backteste tes stratégies avec Stoic Terminal* avant de mettre ton capital en jeu."
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# 📒 Commande /conseil - Conseils aleatoires
async def conseil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "📈 *HODL* : Acheter et conserver à long terme, comme un bon vin qui se bonifie avec le temps. 🍷",
        "⚡ *Surveille les tendances sur X avec LunarCrush et AssetDash* : La hype est ton meilleur indicateur !",
        "🛑 *Ne jamais investir plus que ce que tu es prêt à perdre*.",
        "📉 *Diversifie ton portefeuille* : Ne mets pas tout dans un seul projet, répartis entre plusieurs cryptos solides.",
        "🚨 *Attention aux scams* : Vérifie toujours la source d’un projet avant d’y investir.",
        "🛠️ *Utilise des outils comme Axiom et Stoic Terminal pour automatiser tes trades et optimiser tes entrées.*",
        "📊 *Backteste tes stratégies avant d’investir en réel* : Ne fonce pas tête baissée sur un pump aléatoire !",
        "🌕 *Prends en compte les cycles du marché et les émotions des investisseurs, la lune influence plus qu’on ne le pense !*"
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# Commande /risques - Prevention des risques
async def risques(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "🛑 *Ne jamais investir plus que ce que tu es prêt à perdre*.",
        "🔐 *Stocke tes cryptos sur un cold wallet comme Ledger ou Metamask*.",
        "📉 *Garde toujours 10-20% de ton capital en stablecoin pour les imprévus*.",
        "📌 *Évite les émotions : Pas de FOMO, pas de panique sell, respecte ton plan !*",
        "🔍 *Analyse toujours un projet avant d’investir : Whitepaper, équipe, liquidité.*"
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# 🔥 Commande /scam - Prévention des Arnaques
async def scam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "⚠️ *Méfie-toi des projets promettant des rendements impossibles.*",
        "🧐 *Toujours vérifier le contrat sur Token Sniffer avant d’acheter un shitcoin*.",
        "🚨 *Si un influenceur te force à acheter un token sans info claire, c’est suspect !*",
        "🔗 *Ne clique jamais sur un lien inconnu envoyé en DM sur Telegram ou X.*",
        "🛡️ *Ne jamais partager ta seed phrase. Même Francis ne la demande pas !*"
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# 🤖 Commande /bots - Automatisation et Bots
async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conseils = [
        "🤖 *Utilise Axiom ou Stoic Terminal pour automatiser tes stratégies de trading.*",
        "📡 *ToxiSolBot peut détecter les nouvelles tendances crypto en temps réel !*",
        "⚙️ *BotFather permet de créer et gérer facilement tes bots Telegram pour le trading.*",
        "📱 *Tout ça peut être fait depuis ton smartphone avec Termux, pas besoin de PC !*",
        "📊 *Associe ton bot avec des analyses de Vector ou AssetDash pour optimiser tes trades.*"
    ]
    await update.message.reply_text(random.choice(conseils), parse_mode="Markdown")

# 🌘 Commande /lune - Calendrier lunaire
async def lune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    moon = ephem.Moon()
    moon.compute()
    phase = moon.phase

    if phase < 7.4:
        message = "🌑 Nouvelle Lune : Bon moment pour initier des projets, mais attention à l’incertitude !"
    elif 7.4 <= phase < 14.8:
        message = "🌓 Premier Quartier : Énergie croissante, bonne période pour la prise de décisions."
    elif 14.8 <= phase < 22.1:
        message = "🌕 Pleine Lune : Forte émotion et volatilité sur le marché, prudence !"
    else:
        message = "🌗 Dernier Quartier : Période de réflexion, bon moment pour sécuriser ses profits."

    await update.message.reply_text(message, parse_mode="Markdown")

# 🥛 Commande /milk - Annonces token MILK 
async def milk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🥛 **Francis prépare sa récolte de MILK !** 🚀\n\n"
        "Bientôt, tu pourras accéder à des services avancés de trading et de sniping de tokens grâce à MILK.\n"
        "Francis veut permettre aux investisseurs de **récolter à maturité** sans dépenser des fortunes. 🌾\n\n"
        "🔥 **Reste attentif !** MILK arrive bientôt... Suis les annonces dans Le Club !"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

# Initialisation du bot
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Commandes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("trading", trading))
    app.add_handler(CommandHandler("degen", degen))
    app.add_handler(CommandHandler("risques", trading))
    app.add_handler(CommandHandler("scam", scam))
    app.add_handler(CommandHandler("bots", bots))
    app.add_handler(CommandHandler("lune", lune))
    app.add_handler(CommandHandler("milk", milk))
    app.add_handler(CommandHandler("conseil", conseil))
   
 # Réponses interactives
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interactivity))

    print("✅ Francis est actif et répond aux commandes et interactions !")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
