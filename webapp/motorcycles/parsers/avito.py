from datetime import datetime, timedelta
import locale
import platform

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.motorcycles.models import Motorcycles
from webapp.motorcycles.parsers.utils import get_html, save_data

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')

def parse_moto_date(date_str):
    if 'минут' in date_str:
        today = datetime.now()
        date_str = today.strftime('%d %B %Y')
    elif 'час' in date_str:
        today = datetime.now()
        date_str = today.strftime('%d %B %Y')
    elif '1 день' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%d %B %Y')
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()


def get_moto_snippets():
    html = get_html("https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly-ASgBAgICAUQ80k0?cd=1&s=104&radius=0")
    if html: 
        soup = BeautifulSoup(html, 'html.parser')
        all_moto = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item_table')

        for moto in all_moto:

            title = moto.find('div', class_="snippet-title-row").find('h3').text.strip()
            url = 'https://www.avito.ru' + moto.find('div', class_="snippet-title-row").find('h3').find('a').get('href')
            price = moto.find('div', class_="snippet-price-row").text.strip()
            metro = moto.find('div', class_='data').find('div', class_='item-address').text.strip()
            published = moto.find('div', class_="snippet-date-info").text
            published = parse_moto_date(published)
            save_data(title, url, price, metro, published)


def get_moto_content():
    moto_without_text = Motorcycles.query.filter(Motorcycles.text.is_(None))
    for moto in moto_without_text:
        html = get_html(moto.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            try:
                moto_text = soup.find('div', class_='item-view-content').decode_contents()
            except:
                continue
            if moto_text:
                moto.text = moto_text
                db.session.add(moto)
                db.session.commit()
