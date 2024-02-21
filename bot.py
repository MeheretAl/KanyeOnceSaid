from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from os import getenv
from requests import get


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}!")


async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Contact @lordmhri for assistance")


def kanyeQuotes() -> str:
    url = get("https://api.kanye.rest")
    if url.status_code == 200:
        data = url.json()
        return data["quote"]
    else:
        return "Please try again"


async def kanye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(kanyeQuotes())


def main() -> None:
    application = Application.builder().token(getenv("TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", helpCommand))
    application.add_handler(CommandHandler("kanye", kanye))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
