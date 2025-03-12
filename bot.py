import logging
import asyncio
import time
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# Токен бота и ID канала
BOT_TOKEN = "7385634728:AAG-twcqVUOFRdqa38G7EAZQlbhN2mO3E8E"  # Замените на свой токен
CHANNEL_ID = "-1002332689318"  # Замените на ваш ID канала

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация Flask
app = Flask(__name__)

# Хранение времени последней отправки сплетни
user_last_message_time = {}
spam_timeout = 600  # 10 минут (600 секунд)

# Случайные ответы
def get_random_response(response_type: str) -> str:
    responses = {
        "start": [
            "Привет! Я — бот Сплетник! 🔥\n\n"
            "Здесь можно делиться сплетнями анонимно! Готов слушать, пишите что угодно!\n\n"
            "🚫 Кружки, каналы и группы Telegram запрещены!"
        ],
        "gossip_sent": [
            "Ваша сплетня успешно отправлена! 🔥",
            "Сплетня ушла в канал! Подождите результатов голосования! 😏"
        ],
        "spam_detected": [
            "Вы уже отправили сплетню! Подождите 10 минут перед следующей.",
            "Слишком часто! Следующую сплетню можно отправить через 10 минут."
        ],
        "error": [
            "Что-то пошло не так. Попробуйте снова."
        ]
    }
    return random.choice(responses.get(response_type, ["Ошибка."]))

# Обработка команды /start
@dp.message(Command("start"))
async def process_start_command(message: types.Message):
    response_text = get_random_response("start")
    await message.answer(response_text)

# Обработка текстовых сообщений (сплетни)
@dp.message(F.text)
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Проверка на антиспам (10 минут)
    if user_id in user_last_message_time:
        last_time = user_last_message_time[user_id]
        if current_time - last_time < spam_timeout:
            await message.answer(get_random_response("spam_detected"))
            return

    user_last_message_time[user_id] = current_time  # Обновляем время отправки

    gossip = message.text.strip()
    if gossip:
        try:
            await bot.send_message(CHANNEL_ID, f"Новая сплетня от анонима: {gossip}")

            # Создаем опрос
            await bot.send_poll(
                chat_id=CHANNEL_ID,
                question="Оцените сплетню:",
                options=["✅ Правда", "❌ Ложь"],
                is_anonymous=True,
                type="regular"
            )

            await message.answer(get_random_response("gossip_sent"))

        except Exception as e:
            logging.error(f"Ошибка при отправке в канал: {e}")
            await message.answer(get_random_response("error"))

# Функция для запуска Flask-сервиса для пингов
@app.route('/ping')
def ping():
    return 'OK', 200

# Запуск бота
async def main():
    await dp.start_polling(bot)

# Функция для запуска Flask в отдельном потоке
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    thread = Thread(target=run_flask)
    thread.start()

    # Запускаем бота
    asyncio.run(main())
