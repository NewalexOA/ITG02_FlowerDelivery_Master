import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import register_handlers

# Установить уровень логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчиков
register_handlers(dp)

# Асинхронная функция для запуска бота
async def main():
    await dp.start_polling()

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
