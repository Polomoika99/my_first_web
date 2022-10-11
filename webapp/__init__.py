from flask import Flask, flash, redirect, render_template, url_for #flash - позволяет передавать сообщения между route-ами, 
    #redirect - делает перенаправление пользователя на другую страницу, 
    #url_for - помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import login_required, LoginManager, current_user #login_required - декоратор (Создадим страницу, доступную только зарегистрированным)

from webapp.db import db #Привязываем базу (model.py) к нашему Flask-приложению
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

def create_app():
    app = Flask(__name__) #Создаем переменную app, в которой будет Flask приложением, куда передаем __name__ имя текущего файла для инициализации.
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader #Получаем по id нужного пользователя через запрос к БД
    def load_user(user_id):
        return User.query.get(user_id)


    return app