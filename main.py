import telegram.ext as tge
import telegram as tg
import dotenv
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

dotenv.load_dotenv()

app = tge.ApplicationBuilder().token(os.getenv('ACCESS_TOKEN')).concurrent_updates(True).build()

async def start(update: tg.Update, context: tge.ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Test bot")

app.add_handler(tge.CommandHandler("start", start))

app.run_polling()