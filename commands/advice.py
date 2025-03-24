from telegram import Update
from telegram.ext import ContextTypes
from config.settings import CONSEILS
import random

async def conseil_generic(update: Update, context: ContextTypes.DEFAULT_TYPE, category):
    await update.message.reply_text(random.choice(CONSEILS[category]), parse_mode="Markdown")

async def trading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "trading")

async def degen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "degen")

async def risques(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "risques")

async def scam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "scam")

async def bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "bots")

async def conseil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await conseil_generic(update, context, "conseil")
