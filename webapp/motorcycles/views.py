from flask import Blueprint, render_template
from webapp.motorcycles.models import Motorcycles

blueprint = Blueprint('motorcycles', __name__)

@blueprint.route('/')
def index():
    page_title = 'Клон Авито: Мотоциклы'
    url = "https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?cd=1&radius=0"
    data_avito = Motorcycles.query.order_by(Motorcycles.price.desc()).all()
    return render_template('motorcycles/index.html', page_title=page_title, data_avito=data_avito)