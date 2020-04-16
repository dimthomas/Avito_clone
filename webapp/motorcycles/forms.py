from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from webapp.motorcycles.models import Motorcycles


class CommentForm(FlaskForm):
    moto_id = HiddenField('ID новости', validators=[DataRequired()])
    comment_text = StringField('Ваш комментарий', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_moto_id(self, moto_id):
        if not Motorcycles.query.get(moto_id.data):
            raise ValidationError('Новости с таким id не существует')