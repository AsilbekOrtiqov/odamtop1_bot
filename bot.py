import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# ================== SOZLAMALAR ==================

TOKEN = os.getenv("BOT_TOKEN")  # Railway yoki local CMD uchun

# MANBA GURUHLAR (xabar oladigan guruhlar ID'lari)
SOURCE_GROUPS = [
    -1003611930007,  # manba guruh 1
     7507331298,
     8338678070,
     -5128171267,  # manba guruh 2
    # qo‘shimcha guruhlar shu yerga qo‘shiladi
]

# QABUL QILUVCHI GURUH (target)
TARGET_GROUP_ID = -5253865915

# KALIT SO‘ZLAR
KEYWORDS = [
    "ketaman",
    "bitta kam",
    "bitta kamdamz",
    "NAMANGAN","COBALT","Cobalt","Gentra", "GENTRA","TOSHKENT", "Toshkent", "pochta bor"
]

# TELEFON RAQAM REGEX
PHONE_REGEX = re.compile(r"\b\d{9,13}\b")

# =================================================

logging.basicConfig(level=logging.INFO)


def is_valid_message(text: str) -> bool:
    text_lower = text.lower()

    # kalit so‘zlardan bittasi bo‘lishi shart
    if not any(k in text_lower for k in KEYWORDS):
        return False

    # telefon raqam bo‘lishi shart
    if not PHONE_REGEX.search(text):
        return False

    # joy bo‘lishi uchun kamida 3 ta so‘z bo‘lsin
    if len(text.split()) < 3:
        return False

    return True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    chat_id = msg.chat.id

    # faqat manba guruhlardan oladi
    if SOURCE_GROUPS and chat_id not in SOURCE_GROUPS:
        return

    text = msg.text.strip()

    if not is_valid_message(text):
        return

    # xabarni o‘zgartirmasdan yuboradi
    await context.bot.send_message(
        chat_id=TARGET_GROUP_ID,
        text=text
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Odamtop1 bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()