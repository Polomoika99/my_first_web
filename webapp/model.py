# Модель описывает объект, который мы хотим сохранять в БД и получать из БД. 
# SQLAlchemy будет делать всю работу по переводу с привычного нам python-синтаксиса на язык SQL.

#from enum import unique
from flask_login import UserMixin #Добавим в нашу модель интеграцию с Flask-Login. Мы можем создать эти поля и метод руками, но можно поступить проще и использовать UserMixin.
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash #Работа с паролем, шифруем его без воз-ти расшифровки

db = SQLAlchemy()

class News(db.Model): #Перечисляем поля в модели
    id = db.Column(db.Integer, primary_key=True) #Айди новости
    title = db.Column(db.String, nullable=False) #nullable=True - могут быть новости без этих данных
    url = db.Column(db.String, unique=True, nullable=False) #unique=True - url всегда уникальны по идее
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True) #Текст новости

    def __repr__(self) -> str: #self - обращаемся к объекту класса, который активен
        return '<News {} {}>'.format(self.title, self.url) #При принте выдает в новости {title} и {url}

class User(db.Model, UserMixin): #Модель пользователя
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True) #Роль людей (админ или юзер)

    def set_password(self, password):
        self.password = generate_password_hash(password) #Шифровка пароля ч/з generate_password_hash. В БД идет шифровка.

    def check_password(self, password):
        return check_password_hash(self.password, password) #Возвращает True или False (через шифровку, а не оригинал)
    
    @property
    def is_admin(self):
        return self.role == 'admin' #Декоратор @property позволяет вызывать метод как атрибут, без скобочек. Проверка на админа

    def __repr__(self):
        return '<User name = {} id = {}>'.format(self.username, self.id) #Получаем строчку


