import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web

# Получаем токен и ID канала
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Используй переменную окружения!
CHANNEL_ID = "-1002332689318"  # Замени на ID своего канала

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Вебхук URL
WEBHOOK_HOST = "https://anonimki.onrender.com"
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

# Обработка команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я — бот Сплетник! 🔥\nЗдесь можно делиться сплетнями анонимно!")

# Пересылка сообщений в канал
@dp.message()
async def forward_message(message: Message):
    try:
        forwarded_message = await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"🔥 *Новая сплетня от анонима:*\n\n{message.text}",
            parse_mode="Markdown"
        )

        # Добавляем кнопки голосования
        await bot.send_poll(
            chat_id=CHANNEL_ID,
            question="Оцените сплетню:",
            options=["✅ Правда", "❌ Ложь"],
            is_anonymous=True
        )

        await message.answer("Сплетня отправлена в канал! 🔥")

    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        await message.answer("Ошибка при отправке в канал. Попробуйте снова.")

# Обработка вебхука
async def handle_webhook(request):
    json_str = await request.json()
    update = types.Update(**json_str)
    await dp._update_handlers.notify(update)
    return web.Response()

# Настройка вебхука
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

# Запуск бота
async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    await on_startup()
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

