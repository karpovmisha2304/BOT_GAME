import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from keyboards.main_menu import menu_bot

logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():

    # Загружаем конфиг в переcdменную config
    config: Config = load_config()
    
    # Задаём базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )
    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )          
    dp = Dispatcher()
    await menu_bot(bot)
        
    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
