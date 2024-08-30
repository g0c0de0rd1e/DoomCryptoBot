import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from parser import parse_info  # Импортируем функцию из parser.py
from translations import translations  # Импортируем переводы

load_dotenv()

# Токен бота
TOKEN = os.getenv('TOKEN')

# Максимальная длина сообщения
MAX_MESSAGE_LENGTH = 4096

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token=TOKEN)

# Создаем диспетчер с использованием MemoryStorage
dp = Dispatcher(storage=MemoryStorage())

# Переменная для хранения выбранного языка
user_language = {}

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    language = user_language.get(message.from_user.id, 'en')
    await message.answer(translations["start"][language])

# Обработчик команды /stop
@dp.message(Command(commands=["stop"]))
async def cmd_stop(message: Message):
    language = user_language.get(message.from_user.id, 'en')
    await message.answer(translations["stop"][language])
    await bot.session.close()
    await dp.stop_polling()

# Обработчик команды /set_language
@dp.message(Command(commands=["set_language"]))
async def cmd_set_language(message: Message):
    try:
        lang = message.text.split()[1].lower()
        if lang in translations["start"]:
            user_language[message.from_user.id] = lang
            await message.answer(translations["language_set"][lang])
        else:
            await message.answer("Language not supported.")
    except IndexError:
        await message.answer("Please specify a language. Usage: /set_language <language_code>")

# Обработчик команды /current_language
@dp.message(Command(commands=["current_language"]))
async def cmd_current_language(message: Message):
    language = user_language.get(message.from_user.id, 'en')
    await message.answer(f"{translations['current_language'][language]} {language}")

# Обработчик команды /info
@dp.message(Command(commands=["info"]))
async def cmd_info(message: Message):
    language = user_language.get(message.from_user.id, 'en')
    all_info = await parse_info(language)
    if all_info:
        for info in all_info:
            for i in range(0, len(info), MAX_MESSAGE_LENGTH):
                await message.answer(info[i:i + MAX_MESSAGE_LENGTH], parse_mode='HTML')
    else:
        await message.answer(translations["info_not_found"][language])

# Запуск процесса опроса бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    