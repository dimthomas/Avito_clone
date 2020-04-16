from bs4 import BeautifulSoup

from webapp.db import db
from webapp.motorcycles.models import Motorcycles
from webapp.motorcycles.parsers.utils import get_html, save_data


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
            save_data(title, url, price, metro)


def get_moto_content():
    moto_without_text = Motorcycles.query.filter(Motorcycles.text.is_(None))
    for moto in moto_without_text:
        html = get_html(moto.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            moto_text = soup.find('div', class_='item-view-content').decode_contents()
            if moto_text:
                moto.text = moto_text
                db.session.add(moto)
                db.session.commit()
