from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    subscription_level = db.Column(db.String(20), nullable=False)
    account_status = db.Column(db.String(20), nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    access_level = db.Column(db.String(20), nullable=False)
    available_hours = db.Column(db.String(20), nullable=False)
