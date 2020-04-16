from flask import abort, Blueprint, current_app, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.motorcycles.forms import CommentForm
from webapp.motorcycles.models import Comment, Motorcycles
from webapp.utils import get_redirect_target

blueprint = Blueprint('motorcycles', __name__)

@blueprint.route('/')
def index():
    page_title = 'Клон Авито: Мотоциклы'
    url = "https://www.avito.ru/sankt-peterburg/mototsikly_i_mototehnika/mototsikly?cd=1&radius=0"
    data_avito = Motorcycles.query.filter(Motorcycles.text.isnot(None)).order_by(Motorcycles.price.desc()).all()
    return render_template('motorcycles/index.html', page_title=page_title, data_avito=data_avito)


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
         