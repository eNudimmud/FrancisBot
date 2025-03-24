from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👨‍🌾 **Bienvenue dans Le Club de Francis !** 🚜\n\n"
        "Francis, fermier du canton de Vaud et expert en crypto, est là pour te guider.\n"
        "Tape /help pour voir toutes les commandes disponibles !",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 **Commandes de Francis** 📜\n\n"
        "/start - Démarrer Francis 🚀\n"
        "/help - Voir cette liste\n"
        "/trading - Conseil de trading classique 📈\n"
        "/degen - Conseil pour le trading degen 💸\n"
        "/risques - Conseil sur la gestion des risques 🛡️\n"
        "/scam - Prévention des arnaques ⚠️\n"
        "/bots - Découvrir les outils et bots 🤖\n"
        "/conseil - Obtenir un conseil crypto aléatoire 🎲\n"
        "/lune - Voir l'impact de la lune sur le marché 🌙\n"
        "/swissmilk - Découvrir la future tokenisation de Francis 🥛\n"
        "/prix - Voir le prix actuel d’une crypto (ex. /prix BTC) 💰\n"
        "/portefeuille - Gérer ton champ simulé (ajouter, voir, stats, retirer, top)\n"
        "/milk - Voir ton $MILK et $CHEESE\n"
        "/stack - Stacker ton $MILK en $CHEESE (simulation)\n"
        "/nft - Découvrir les futurs NFT Highland",
        parse_mode="Markdown"
    )

async def interactivity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    responses = {
        "bonjour": ["👨‍🌾 Salut l’ami ! Une belle journée pour cultiver du BTC ! 🌾"],
        "comment vas-tu": ["📈 Tant que le marché n’est pas en bear market, tout va bien !"],
        "aurevoir": ["👨‍🌾 À plus tard l’ami ! Que tes récoltes de crypto soient abondantes ! 🌾"],
        "salut": ["👨‍🌾 Salut mon gars ! Toujours dans la ferme ou sur les marchés ? 🚀"],
        "oh con francis": ["😆 Oh con ! T'es là toi ? J'étais en train de surveiller mes cryptos et mes vaches !"]
    }
    for key, messages in responses.items():
        if key in text:
            await update.message.reply_text(random.choice(messages))
            return
