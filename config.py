import os
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

if not BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing credentials in .env file")

MAX_FILE_SIZE_MB = 2000
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
GROQ_MODEL = "whisper-large-v3"

TEMP_DIR = os.getenv("TEMP_DIR", "/root/projects/sharing/tg-voicebot/")
BOT_API_URL = os.getenv("BOT_API_URL", "https://api.telegram.org")
DB_PATH = "voice_stats.db"

class UI:
    START_MESSAGE = (
        "👋 <b>Привет! Я VoiceBot.</b>\n\n"
        "Просто перешли мне или отправь:\n"
        "🎤 Голосовое сообщение\n"
        "📹 Видео или Кружочек\n\n"
        "Я моментально расшифрую речь в текст с помощью ИИ!"
    )
    PROCESSING = "⏳ <i>Слушаю и расшифровываю...</i>"
    SUCCESS_TITLE = "💬 <b>Текст расшифрован!</b>"
    FILE_TOO_BIG = f"❌ Файл слишком большой! Пожалуйста, отправляйте файлы до {MAX_FILE_SIZE_MB} МБ."
    ERROR_GENERIC = "⚠️ Произошла ошибка при обработке файла. Попробуйте позже."
    BTN_SHOW = "Показать текст"
    BTN_HIDE = "Скрыть текст"
    ERR_NOT_FOUND = "Текст не найден (возможно бот был перезагружен)."

def setup_logging() -> None:
    """Configure application logging system."""
    log_format = "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler()]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.INFO)