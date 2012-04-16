from flask.ext.sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    access_token = db.Column(db.String)
    access_token_secret = db.Column(db.String)

    def __init__(self, email, first_name,
                 last_name, access_token, access_token_secret):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def __repr__(self):
        return "<User {0}>".format(self.email)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
