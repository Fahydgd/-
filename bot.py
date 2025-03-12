import logging
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Токен бота и ID канала
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Замените на свой токен или используйте переменную окружения
CHANNEL_ID = "-1002332689318"  # Замените на ваш ID канала

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Вебхук URL
WEBHOOK_HOST = 'https://anonimki.onrender.com'  # URL вашего Render приложения
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

# Устанавливаем вебхук
async def on_start_webhook(request):
    return web.Response(text="Webhook is set")

async def on_webhook(request):
    json_str = await request.json()
    update = types.Update(**json_str)
    await dp.process_update(update)
    return web.Response()

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет! Я — бот Сплетник! 🔥\nЗдесь можно делиться сплетнями анонимно!")

# Обработка текстовых сообщений (сплетни)
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
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

            await message.answer("Сплетня отправлена! 🔥")
        except Exception as e:
            logging.error(f"Ошибка при отправке в канал: {e}")
            await message.answer("Что-то пошло не так. Попробуйте снова.")

# Запуск вебхука
async def on_start(request):
    return web.Response(text="Webhook setup successfully.")

async def setup():
    # Настройка webhook
    await bot.set_webhook(WEBHOOK_URL)

# Основная функция для работы с aiohttp
def main():
    app = web.Application()
    app.router.add_get('/', on_start_webhook)
    app.router.add_post(f'/{BOT_TOKEN}', on_webhook)

    # Настроить webhook
    web.run_app(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

if __name__ == '__main__':
    main()
