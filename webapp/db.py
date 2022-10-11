# Модель описывает объект, который мы хотим сохранять в БД и получать из БД. 
# SQLAlchemy будет делать всю работу по переводу с привычного нам python-синтаксиса на язык SQL.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

