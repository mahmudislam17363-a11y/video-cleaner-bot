
import os
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Bot Token will be loaded from hosting environment
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "স্বাগতম! 🎬\n\n"
        "আমাকে একটি Forward করা ভিডিও পাঠান।\n"
        "আমি Caption এবং Button ছাড়া ভিডিওটি ফেরত পাঠাব।"
    )


async def clean_video(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    msg = update.effective_message
    chat_id = update.effective_chat.id

    try:
        if msg.video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=msg.video.file_id,
                caption=None,
                supports_streaming=True
            )

        elif msg.document and (
            msg.document.mime_type or ""
        ).startswith("video/"):
            await context.bot.send_document(
                chat_id=chat_id,
                document=msg.document.file_id,
                caption=None
            )

        else:
            await msg.reply_text(
                "দয়া করে একটি ভিডিও পাঠান।"
            )

    except Exception:
        logger.exception("Video sending failed")
        await msg.reply_text(
            "দুঃখিত! ভিডিও পাঠানো যায়নি। আবার চেষ্টা করুন।"
        )


async def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing!"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.VIDEO | filters.Document.VIDEO,
            clean_video
        )
    )

    logger.info("Akash Video Cleaner Bot is starting...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
