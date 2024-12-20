from app import db  # Импортируем объект db из app.py
from app import create_app  # Если у вас есть функция для создания приложения

app = create_app()  # Создаём экземпляр приложения

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()  # Этот метод создаст таблицы, если они ещё не существуют
    print("Все таблицы созданы")
