from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    subscription_level = db.Column(db.String(20), nullable=False)
    account_status = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Хешируем пароль

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Проверяем хеш пароля

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    access_level = db.Column(db.String(20), nullable=False)
    available_hours = db.Column(db.String(20), nullable=False)
