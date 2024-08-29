import asyncio
import logging
import aiohttp
import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from bs4 import BeautifulSoup

# URL для парсинга
url = 'https://airdrops.io/'

# Максимальная длина сообщения
MAX_MESSAGE_LENGTH = 4096

# Асинхронный запрос к URL и парсинг с помощью BeautifulSoup
async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_info():
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_page(session, url)
        soup = BeautifulSoup(response_text, 'lxml')

        all_info = ''
        links = []
        
        # Сбор всех ссылок на страницы airdrops
        for quote in soup.find_all('div', class_='air-content-front'):
            link = quote.find('a')
            if link:
                links.append(link.get('href'))

        # Переход по каждой ссылке и парсинг информации
        for link in links:
            response_text = await fetch_page(session, link)
            page_soup = BeautifulSoup(response_text, 'lxml')
            
            title = page_soup.find('h1').text if page_soup.find('h1') else 'No title found'
            inf = page_soup.find('div', class_='grid-60 grid-parent').text if page_soup.find('div', class_='grid-60 grid-parent') else 'No information found'
            lin = page_soup.find('a', class_='claim-airdrop button outline')
            lin_href = lin.get('href') if lin else 'No link found'

            all_info += f"Title: {title}\nInfo: {inf}\nLink: {lin_href}\n\n"

        return all_info

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем объект бота
bot = Bot(token="7164929735:AAHodDuQlOy4zO8ttfXB4zQffhum_LKio5A")

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
            await message.answer(all_info[i:i + MAX_MESSAGE_LENGTH])
    else:
        await message.answer("Информация не найдена.")

# Запуск процесса опроса бота
async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())