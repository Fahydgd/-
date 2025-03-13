import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Токен бота и ID канала
BOT_TOKEN = os.getenv("7385634728:AAG-twcqVUOFRdqa38G7EAZQlbhN2mO3E8E")  # Замените на свой токен или используйте переменную окружения
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
start_messages = [
    "Привет! Я — бот Сплетник! 🔥\nЗдесь можно делиться сплетнями анонимно!",
    "Добро пожаловать в мир слухов и тайн! 🤫\nРасскажи, что у тебя на уме!",
    "Хочешь поделиться чем-то пикантным? 😏\nТы в нужном месте!",
    "Анонимность гарантирована! 🔥\nЧто за сплетню ты принес сегодня?",
]

# Обработка текстовых сообщений (сплетни)
@dp.message()
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

# Обработка медиафайлов
@dp.message(lambda message: message.content_type == ContentType.PHOTO)
async def handle_photo(message: types.Message):
    try:
        media = message.photo[-1].file_id  # Берем фото с лучшим качеством
        caption = "Фото от анонима!"
        await bot.send_photo(chat_id=CHANNEL_ID, photo=media, caption=caption)
        await message.answer("Медиа отправлено в канал! 🎬")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке фото: {e}")
        await message.answer("Ошибка при отправке фото. Попробуйте снова.")

@dp.message(lambda message: message.content_type == ContentType.VIDEO)
async def handle_video(message: types.Message):
    try:
        media = message.video.file_id  # Берем видео
        caption = "Видео от анонима!"
        await bot.send_video(chat_id=CHANNEL_ID, video=media, caption=caption)
        await message.answer("Медиа отправлено в канал! 🎬")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке видео: {e}")
        await message.answer("Ошибка при отправке видео. Попробуйте снова.")

@dp.message(lambda message: message.content_type == ContentType.VOICE)
async def handle_voice(message: types.Message):
    try:
        media = message.voice.file_id  # Берем голосовое сообщение
        caption = "Голосовое сообщение от анонима!"
        await bot.send_voice(chat_id=CHANNEL_ID, voice=media, caption=caption)
        await message.answer("Медиа отправлено в канал! 🎬")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке голосового сообщения: {e}")
        await message.answer("Ошибка при отправке голосового сообщения. Попробуйте снова.")

from aiogram.filters import Command
from aiohttp import web

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
