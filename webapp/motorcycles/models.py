from datetime import datetime
from sqlalchemy.orm import relationship

from webapp.db import db


class Motorcycles(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False)
        url = db.Column(db.String, unique=True, nullable=False)
        price = db.Column(db.String, nullable=False)
        metro = db.Column(db.String, nullable=False)
        published = db.Column(db.DateTime, nullable=True)
        text = db.Column(db.Text, nullable=True)

        def comments_count(self):
            return Comment.query.filter(Comment.moto_id == self.id).count()

        def __repr__(self):
            return '<Motorcycles {} {}>'.format(self.title, self.url)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    moto_id = db.Column(
    db.Integer,
    db.ForeignKey('motorcycles.id', ondelete='CASCADE'),
    index=True
    )
    user_id = db.Column(
    db.Integer,
    db.ForeignKey('user.id', ondelete='CASCADE'),
    index=True
    )
    moto = relationship('Motorcycles', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
        