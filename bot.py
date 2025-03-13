import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен бота и ID канала
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Используй переменную окружения!
if not BOT_TOKEN:
    logging.critical("❌ Токен бота не найден! Укажите его в переменных окружения.")
    exit(1)

CHANNEL_ID = "-1002332689318"  # Замени на свой ID канала

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# URL вебхука
WEBHOOK_HOST = "https://anonimki.onrender.com"
WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    logging.info(f"✅ Получена команда /start от {message.from_user.id}")
    await message.answer("Привет! Я — бот Сплетник! 🔥\nЗдесь можно делиться сплетнями анонимно!")

# Пересылка сообщений в канал
@dp.message()
async def forward_message(message: types.Message):
    logging.info(f"📩 Получено сообщение: {message.text}")
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"🔥 *Новая сплетня от анонима:*\n\n{message.text}",
            parse_mode="Markdown"
        )
        await message.answer("Сплетня отправлена в канал! 🔥")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке в канал: {e}")
        await message.answer("Ошибка при отправке в канал. Попробуйте снова.")

# Обработка вебхука
async def handle_webhook(request):
    json_str = await request.json()
    update = types.Update(**json_str)
    logging.info(f"🔔 Получено обновление: {update}")
    await dp.feed_update(bot, update)
    return web.Response()

# Установка вебхука
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")

# Остановка бота
async def on_shutdown():
    await bot.session.close()
    logging.info("🛑 Бот остановлен")

# Запуск бота
async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    await on_startup()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 5000)))
    await site.start()

    logging.info("🚀 Бот запущен и ждет обновлений!")
    
    try:
        while True:
            await asyncio.sleep(3600)  # Бесконечный цикл ожидания
    except (KeyboardInterrupt, SystemExit):
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
