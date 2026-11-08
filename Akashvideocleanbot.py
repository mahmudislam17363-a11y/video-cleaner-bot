
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["9025714702:AAHe3jB9tAgfjDCluvEtrTc3JMV6PLE8wz8"]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a forwarded video. "
        "I will return it without caption or buttons."
    )

async def clean_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message

    try:
        if msg.video:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=msg.video.file_id,
                caption=None,
                supports_streaming=True
            )

        elif msg.document and (
            msg.document.mime_type or ""
        ).startswith("video/"):
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=msg.document.file_id,
                caption=None
            )

        else:
            await msg.reply_text("Please forward a video.")

    except Exception:
        logging.exception("Video sending failed")
        await msg.reply_text("Sorry, video could not be processed.")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.VIDEO | filters.Document.ALL,
            clean_video
        )
    )
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    import os
    asyncio.run(main())
