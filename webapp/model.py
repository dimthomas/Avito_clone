from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Motorcycles(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String, nullable=False)
        url = db.Column(db.String, unique=True, nullable=False)
        price = db.Column(db.String, nullable=False)
        metro = db.Column(db.String, nullable=False)

        def __repr__(self):
            return '<Motorcycles {} {}>'.format(self.title, self.url)