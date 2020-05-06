from datetime import datetime
from flask import abort, Blueprint, current_app, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.motorcycles.forms import CommentForm, AdForm
from webapp.motorcycles.models import Comment, Motorcycles
from webapp.utils import get_redirect_target

blueprint = Blueprint('motorcycles', __name__)

@blueprint.route('/create', methods=['POST', 'GET'])
def create_ad():

    '''if request.method == 'POST':
        title = request.form['title']
        metro = request.form['metro']
        price = request.form['price']
        body = request.form['body']
        try:
            ad = Motorcycles(title=title, metro=metro, price=price, url=None, text=body, published=datetime.now())
            db.session.add(ad)
            db.session.commit()
            flash('Объявление добавлено')
        except:
            print('Что-то пошло не так')
        return redirect(get_redirect_target())'''
    
    form = AdForm()
    return render_template('motorcycles/create_ad.html', form=form)


@blueprint.route('/')
def index():

    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    '''if q:
        data_avito = Motorcycles.query.filter(Motorcycles.title.contains(q)).all()
    else:'''

    page_title = 'Клон Авито: Мотоциклы'
    url = "https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?cd=1&radius=0"
    
    if q:
        data_avito = Motorcycles.query.filter(Motorcycles.title.contains(q)) #.all()
    else:
        data_avito = Motorcycles.query.filter(Motorcycles.text.isnot(None)).order_by(Motorcycles.published.desc())

    pages = data_avito.paginate(page=page, per_page=5)

    return render_template('motorcycles/index.html', page_title=page_title, pages=pages)


@blueprint.route('/moto/<int:moto_id>')
def single_moto(moto_id):
    my_moto = Motorcycles.query.filter(Motorcycles.id == moto_id).first()

    if not my_moto:
        abort(404)
    comment_form = CommentForm(moto_id=my_moto.id)
    return render_template('motorcycles/single_moto.html', page_title=my_moto.title, moto=my_moto, comment_form=comment_form)


@blueprint.route('/moto/comment', methods=['POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.comment_text.data, moto_id=form.moto_id.data, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())
         