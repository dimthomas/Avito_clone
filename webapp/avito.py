import requests
from bs4 import BeautifulSoup
import csv

from webapp.db import db
from webapp.motorcycles.models import Motorcycles

def get_html(url):
    try:
        result =requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

'''def write_csv(data):
    with open('avito.csv', 'a', encoding='utf8') as f:
        write_file = csv.writer(f)
        write_file.writerow( (data['title'],
                              data['price'],
                              data['metro'],
                              data['url']) )'''


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item_table')

#TODO: Сделать проверку при помощи if

    for ad in ads:
        title=price=metro=url = None

        if ad.find('div', class_="snippet-title-row js-snippet-title-row"):
            title = ad.find('div', class_="snippet-title-row js-snippet-title-row").find('h3').text.strip()
        if 'https://www.avito.ru' + ad.find('div', class_="snippet-title-row js-snippet-title-row").find('h3').find('a').get('href'):
            url = 'https://www.avito.ru' + ad.find('div', class_="snippet-title-row js-snippet-title-row").find('h3').find('a').get('href')
        if ad.find('div', class_="snippet-price-row"):
            price = ad.find('div', class_="snippet-price-row").text.strip()
        if ad.find('div', class_='data').find('div', class_='item-address'):
            metro = ad.find('div', class_='data').find('div', class_='item-address').text.strip()

        save_data(title, url, price, metro)

def save_data(title, url, price, metro):
    url_exists = Motorcycles.query.filter(Motorcycles.url == url ).count()
    if not url_exists:
        moto = Motorcycles(title=title, url=url, price=price, metro=metro)
        db.session.add(moto)
        db.session.commit()


def get_all_url():
    url = "https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?cd=1&radius=0"
    base_url = 'https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)
