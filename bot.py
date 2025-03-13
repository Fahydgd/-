import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import random

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

# Разнообразные приветственные сообщения
start_messages = [
    "Привет! Я — бот Сплетник! 🔥\nЗдесь можно делиться сплетнями анонимно!",
    "Добро пожаловать в мир слухов и тайн! 🤫\nРасскажи, что у тебя на уме!",
    "Хочешь поделиться чем-то пикантным? 😏\nТы в нужном месте!",
    "Анонимность гарантирована! 🔥\nЧто за сплетню ты принес сегодня?"
]

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    logging.info(f"✅ Получена команда /start от {message.from_user.id}")
    await message.answer(random.choice(start_messages))

# Обработка картинок, видео и видеокружков
@dp.message(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    logging.info(f"📸 Получена фотография от {message.from_user.id}")
    try:
        # Пересылаем фото в канал
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=message.photo[-1].file_id,  # Самое большое фото
            caption=f"🔥 *Новая сплетня от анонима с фото:*",
            parse_mode="Markdown"
        )
        await message.answer("Фото отправлено в канал! 🔥")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке фото: {e}")
        await message.answer("Ошибка при отправке фото. Попробуйте снова.")

@dp.message(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    logging.info(f"🎥 Получено видео от {message.from_user.id}")
    try:
        # Пересылаем видео в канал
        await bot.send_video(
            chat_id=CHANNEL_ID,
            video=message.video.file_id,
            caption=f"🔥 *Новая сплетня от анонима с видео:*",
            parse_mode="Markdown"
        )
        await message.answer("Видео отправлено в канал! 🔥")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке видео: {e}")
        await message.answer("Ошибка при отправке видео. Попробуйте снова.")

@dp.message(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    logging.info(f"🎬 Получено видео заметка от {message.from_user.id}")
    try:
        # Пересылаем видеозаметку в канал
        await bot.send_video_note(
            chat_id=CHANNEL_ID,
            video_note=message.video_note.file_id,
            caption=f"🔥 *Новая сплетня от анонима с видеозаметкой:*",
            parse_mode="Markdown"
        )
        await message.answer("Видеозаметка отправлена в канал! 🔥")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке видеозаметки: {e}")
        await message.answer("Ошибка при отправке видеозаметки. Попробуйте снова.")

# Пересылка текстовых сообщений в канал
@dp.message(content_types=types.ContentType.TEXT)
async def forward_message(message: types.Message):
    logging.info(f"📩 Получено текстовое сообщение: {message.text}")
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
