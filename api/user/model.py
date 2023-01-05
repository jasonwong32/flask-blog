from api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    email_sent = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
