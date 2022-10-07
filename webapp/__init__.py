#from crypt import methods
from flask import Flask, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, redirect - делает перенаправление пользователя на другую страницу, url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import LoginManager, login_required,current_user, login_user, logout_user #LoginManager - главный объект во flask_login, занимается менеджемнетом всего процесса логина
#login_required - декоратор (Создадим страницу, доступную только зарегистрированным)

from webapp.forms import LoginForm
from webapp.model import db, News, User #Привязываем базу (model.py) к нашему Flask-приложению
#from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__) #Создаем переменную app, в которой будет Flask приложением, куда передаем __name__ имя текущего файла для инициализации.
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader #Получаем по id нужного пользователя через запрос к БД
    def load_user(user_id):
        return User.query.get(user_id)

    #Flask использует пути, надо привязать функцию обработчик к какому-то пути на сайте
    @app.route('/') #Декоратор позволяет функции открываться, когда пользователь зайдет на главную страницу сайта

    def index(): #Функция возвращает текст, который нужно вывести на сайте
        title = "Жизнь Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        #weather = False  #Если дать такое значение, выйдет "Сервис погоды временно недоступен". Причем при запущенном файле все обновится автоматом и выдаст на сайте.
        news_list = News.query.order_by(News.published.desc()).all() #Верни все новости из БД. order_by(News.published.desc - сортировка по дате от большего к меньшему
        #Теперь этот код не нужен, когда в index.html прописали  Погода: {{ weather.temp_C }}, ощущается как {{ weather.FeelsLikeC }}
        """if weather : #Проверяем, что weather действительно вернулся, а не False.
            weather_text =  f"Погода: {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}" #Надо вставить внутрь строки часть данных, которые пролучили в weather.
        else :
            weather_text = "Сервис погоды временно недоступен" """
        
        
        return render_template('index.html', page_title = title, weather12 = weather, news_list = news_list)

    @app.route('/login')
    def login():
        print(current_user)
        if current_user.is_authenticated: 
            return redirect(url_for('index')) # Если пользователь уже авторизован и по какой-то причине зашел на /login - перенаправим его на главную:
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)


    @app.route('/process-login', methods = ['POST']) #По умолчанию route обрабатывает только метод get. Мы хотим только метод POST
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user) #Запоминаем пользователя, если успешно вошел на сайт
                flash('Вы успешно вошли на сайт') #Создали сообщение
                return redirect(url_for('index')) #Переадресовали на главную сSтраницу

        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required #Если пользователь не аутентифицирован, то перебрасывает на логин.
    def admin_index():
        if current_user.is_admin:
            return 'Hi, admin.'
        else:
            return 'You are not a admin'

    return app