from telegram.ext import CommandHandler,MessageHandler,Application,filters,ContextTypes
from telegram import ForceReply,Update

import logging
import httpx
from dotenv import load_dotenv
import os

load_dotenv()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
TOKEN = os.getenv("TOKEN")

async def start(update:Update,contetx:ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html}",
        reply_markup= ForceReply(selective=True),
    )

async def kanye_quotes() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.kanye.rest/")
        if response.status_code == 200:
            data = response.json()
            return data["quote"]
        else:
            return "Please try again."
        
async def kanye(update:Update,context : ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(await kanye_quotes)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("help",help))
    application.add_handler(CommandHandler("kanye", kanye))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
