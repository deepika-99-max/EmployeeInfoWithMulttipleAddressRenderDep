from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    addresses = db.relationship('Address', backref='user', cascade="all, delete")

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
