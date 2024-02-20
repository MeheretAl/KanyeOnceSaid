
from telegram.ext import ContextTypes, CommandHandler,Application
from telegram import Update
from os import getenv
from requests import get

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(rf"Hello {update.message.from_user}!")

def kanyeQuotes() -> str:
    url = get("https://api.kanye.rest")
    if url.status_code == 200:
        data = url.json()
        return data["quote"]
    else:
        return "Please try again"

async def kanye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(kanyeQuotes())

async def main() -> None:
    application = Application.builder().token(getenv("TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("kanye", kanye))

    await application.bot.set_webhook(url=getenv("WEBHOOK_URL"))

    async with application:
        await application.run_until_shutdown()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
