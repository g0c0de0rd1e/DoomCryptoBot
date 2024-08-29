import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from parser import parse_info  # Импортируем функцию из parser.py

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

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer("Привет!")

# Обработчик команды /stop
@dp.message(Command(commands=["stop"]))
async def cmd_stop(message: Message):
    await message.answer("Пока!")
    await bot.session.close()
    await dp.stop_polling()

# Обработчик команды /info
@dp.message(Command(commands=["info"]))
async def cmd_info(message: Message):
    all_info = await parse_info()
    if all_info:
        for i in range(0, len(all_info), MAX_MESSAGE_LENGTH):
            await message.answer(all_info[i:i + MAX_MESSAGE_LENGTH], parse_mode='HTML')
    else:
        await message.answer("Информация не найдена.")

# Запуск процесса опроса бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
