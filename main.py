import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler
import handlers

def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)
        
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.critical("No BOT_TOKEN environment variable found. Terminating.")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("help", handlers.help))
    app.add_handler(InlineQueryHandler(handlers.inline_query))

    app.run_polling()

if __name__ == "__main__":
    main()