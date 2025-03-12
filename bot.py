import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Токен бота и ID канала
BOT_TOKEN = "7385634728:AAG-twcqVUOFRdqa38G7EAZQlbhN2mO3E8E"  # Замените на свой токен
CHANNEL_ID = "-1002332689318"  # Замените на ваш ID канала

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Пример использования переменной окружения для порта
from aiohttp import web
port = int(os.getenv("PORT", 8080))  # Используем переменную окружения или порт по умолчанию 8080

# Хранение времени последней отправки сплетни
user_last_message_time = {}
spam_timeout = 600  # 10 минут (600 секунд)

# Обработка команды /start
@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    response_text = "Привет! Я — бот Сплетник! 🔥\n\nЗдесь можно делиться сплетнями анонимно!"
    await message.answer(response_text)

# Запуск бота
async def start():
    await dp.start_polling(bot)

# Основной код для запуска веб-сервиса
app = web.Application()
app.add_routes([web.post('/webhook', start)])

if __name__ == "__main__":
    from aiohttp import web
    web.run_app(app, port=port)  # Используем порт из переменной окружения
