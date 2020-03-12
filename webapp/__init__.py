from flask import Flask, render_template

from webapp.model import db, Motorcycles


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        page_title = 'Клон Авито: Мотоциклы'
        url = "https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?cd=1&radius=0"
        data_avito = Motorcycles.query.order_by(Motorcycles.price.desc()).all()
        return render_template('index.html', page_title=page_title, data_avito=data_avito)
    return app