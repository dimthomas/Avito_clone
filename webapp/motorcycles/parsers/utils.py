import requests

from webapp.db import db
from webapp.motorcycles.models import Motorcycles


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
    }
    try:
        result =requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def save_data(title, url, price, metro, published):
    url_exists = Motorcycles.query.filter(Motorcycles.url == url ).count()
    if not url_exists:
        moto = Motorcycles(title=title, url=url, price=price, metro=metro, published=published)
        db.session.add(moto)
        db.session.commit()
