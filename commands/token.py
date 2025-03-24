from telegram import Update
from telegram.ext import ContextTypes
from config.settings import MILK, CHEESE, MILK_FILE, CHEESE_FILE
from utils.helpers import save_json

async def milk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    milk_amount = MILK.get(user_id, 0)
    cheese_amount = CHEESE.get(user_id, 0)
    await update.message.reply_text(
        f"🥛 Ton stock de $MILK : {milk_amount} unités\n"
        f"🧀 Ton stock de $CHEESE : {cheese_amount:.3f} unités\n"
        "Chaque action dans ton champ te rapporte du $MILK. Stacke-le avec /stack !",
        parse_mode="Markdown"
    )

async def stack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if not context.args:
        await update.message.reply_text("🚜 Usage : /stack <quantité de $MILK> (ex. /stack 99)")
        return
    try:
        milk_to_stack = int(context.args[0])
        if milk_to_stack <= 0 or milk_to_stack < 99 or milk_to_stack > MILK.get(user_id, 0):
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Quantité invalide ou insuffisante (min 99 $MILK) !")
        return

    base_cheese = (milk_to_stack / 99) * 6.854
    MILK[user_id] -= milk_to_stack
    CHEESE[user_id] = CHEESE.get(user_id, 0) + base_cheese
    save_json(MILK_FILE, MILK)
    save_json(CHEESE_FILE, CHEESE)

    await update.message.reply_text(
        f"🧀 [SIMULATION] Tu as stacké {milk_to_stack} $MILK pour {base_cheese:.3f} $CHEESE !\n"
        "Le stacking réel arrive avec les services premium et NFT Highland."
    )

async def nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐮 **Chers amis, parlons des NFT Highland,** dit Francis, votre serviteur du canton de Vaud. 🚜\n"
        "Dans ma ferme numérique, je travaille avec cœur pour vous offrir un projet sincère. Voici ce que je prépare :\n"
        "- **Le projet ?** Chaque NFT sera une vache Highland dessinée à la main, avec soin. Une base solide, agrémentée de chapeaux élégants ou de cloches discrètes, de motifs variés – taches classiques ou rayures audacieuses –, et de décors inspirés de nos terres : prés verdoyants, montagnes majestueuses, ciels dorés. Des milliers de combinaisons possibles, toutes uniques.\n"
        "- **Comment les obtenir ?** Ils s’achèteront avec du $CHEESE, fruit de votre patience à stacker le $MILK. Préparez-vous dès maintenant.\n"
        "- **Leur valeur ?** Ces vaches veilleront sur vos gains avec deux bienfaits : un pourcentage supplémentaire de $CHEESE en stackant votre $MILK (Commun +20%, Peu Commun +40%, Rare +70%, Légendaire +100%), et un pourcentage accru de $MILK lors de vos transactions (Commun +10%, Peu Commun +15%, Rare +20%, Légendaire +25%). Les atouts – d’un simple collier à des joyaux alpins – refléteront leur rang, les légendaires portant votre empreinte personnelle.\n"
        "- **Leur arrivée ?** Elles paîtront dans vos champs lorsque les services premium s’épanouiront et que les premiers NFT verront le jour. D’ici là, entraînez-vous en simulation.\n"
        "Cultivez avec moi, mes amis, je vous guide avec soin vers cette belle aventure ! 🌾"
    )
