from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Resource
import datetime

# Создание приложения Flask
app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', title="Главная страница")

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        subscription_level = request.form.get('subscription_level')
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400

        # Проверка, существует ли уже такой пользователь
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким именем уже существует!", 400
        
        # Создание нового пользователя
        new_user = User(username=username, subscription_level=subscription_level, account_status="active")
        new_user.set_password(password)  # Хешируем пароль

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # После регистрации перенаправляем на страницу логина
    
    return render_template('register.html')

# Авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # Сохраняем id пользователя в сессии
            return redirect(url_for('resources'))  # Перенаправляем на страницу ресурсов
        else:
            return "Неверное имя пользователя или пароль", 400  # Ошибка при неправильном пароле
    
    return render_template('login.html')

# Маршрут для страницы добавления ресурса
@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        access_level = request.form['access_level']
        available_hours = request.form['available_hours']
        
        # Создаем новый объект ресурса
        new_resource = Resource(name=name, access_level=access_level, available_hours=available_hours)
        
        # Добавляем объект в сессию и сохраняем в базе данных
        db.session.add(new_resource)
        db.session.commit()
        
        # Перенаправляем на страницу с ресурсами
        return redirect(url_for('resources'))
    
    return render_template('add_resource.html')

# Страница с доступными ресурсами
@app.route('/resources')
def resources():
    user_id = session.get('user_id')  # Получаем id пользователя из сессии
    if not user_id:
        return redirect(url_for('login'))  # Если пользователь не авторизован, перенаправляем на страницу логина

    user = User.query.get(user_id)  # Получаем пользователя по id из сессии
    current_time = datetime.datetime.now().strftime('%H:%M')  # Получаем текущее время в формате ЧЧ:ММ

    resources = Resource.query.all()  # Получаем все ресурсы из базы данных
    available_resources = []

    for resource in resources:
        # Разделяем доступное время на два значения (начало и конец)
        start_time, end_time = resource.available_hours.split('-')

        # Проверка, соответствует ли уровень доступа пользователя и доступное время
        if (user.subscription_level == resource.access_level or user.subscription_level == 'premium') and \
           start_time <= current_time <= end_time:
            available_resources.append(resource)

# Конкретный ресурс
@app.route('/resources/<int:resource_id>', methods=['GET'])
def resource_detail(resource_id):
    # Получение ресурса по ID
    resource = Resource.query.get_or_404(resource_id)
    return render_template('resource_detail.html', title=resource.name, resource=resource)

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Удаляем данные о пользователе из сессии
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)
