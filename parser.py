import aiohttp
from bs4 import BeautifulSoup
import random
import io
import os
from dotenv import load_dotenv
from googletrans import Translator
from translations import translations  # Импортируем переводы

load_dotenv()

# URL для парсинга
URL = os.getenv('URL')

# Асинхронный запрос к URL и парсинг с помощью BeautifulSoup
async def fetch_page(session, URL):
    async with session.get(URL) as response:
        return await response.text()

async def parse_info(language='en'):
    async with aiohttp.ClientSession() as session:
        response_text = await fetch_page(session, URL)
        soup = BeautifulSoup(response_text, 'lxml')

        drops = []
        
        # Сбор всех ссылок на страницы airdrops
        for quote in soup.find_all('div', class_='air-content-front'):
            link = quote.find('a')
            if link:
                drops.append(link.get('href'))

        # Перемешивание списка ссылок
        random.shuffle(drops)

        all_info = []
        translator = Translator()
        
        # Переход по каждой ссылке и парсинг информации
        for link in drops:
            response_text = await fetch_page(session, link)
            page_soup = BeautifulSoup(response_text, 'lxml')
            
            title = page_soup.find('h1').text if page_soup.find('h1') else 'No title found'
            inf = page_soup.find('div', class_='grid-60 grid-parent').text if page_soup.find('div', class_='grid-60 grid-parent') else 'No information found'
            lin = page_soup.find('a', class_='claim-airdrop button outline')
            lin_href = lin.get('href') if lin else 'No link found'

            if language == 'ru':
                title = translator.translate(title, dest='ru').text
                inf = translator.translate(inf, dest='ru').text if inf else 'Информация не найдена'

            # Проверка на наличие ключа 'all-translations'
            translated_parts = translator.translate(inf, dest='ru').extra_data.get('all-translations', [])
            inf = ' '.join(part.text.strip() for part in translated_parts if part and part.text is not None)

            all_info.append(f"{translations['title'][language]}: {title}\n{translations['info'][language]}: {inf}\n{translations['link'][language]}: <a href='{lin_href}'>{lin_href}</a>")

        return all_info
