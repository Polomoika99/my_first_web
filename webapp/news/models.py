from webapp.db import db

class News(db.Model): #Перечисляем поля в модели
    id = db.Column(db.Integer, primary_key=True) #Айди новости
    title = db.Column(db.String, nullable=False) #nullable=True - могут быть новости без этих данных
    url = db.Column(db.String, unique=True, nullable=False) #unique=True - url всегда уникальны по идее
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True) #Текст новости

    def __repr__(self) -> str: #self - обращаемся к объекту класса, который активен
        return '<News {} {}>'.format(self.title, self.url) #При принте выдает в новости {title} и {url}
