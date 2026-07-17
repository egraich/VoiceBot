import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import config
from handlers import router

async def main():
    """
    Main function.
    """

    config.setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Инициализация VoiceBot v1...")
    
    bot = Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    dp.include_router(router)
    
    try:
        logger.info("Бот успешно запущен и начал слушать обновления (Polling).")

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {e}", exc_info=True)
    finally:
        logger.info("Остановка бота...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот принудительно остановлен (Ctrl+C).")