from flask import Flask, render_template

from webapp.model import db, News #Привязываем базу (model.py) к нашему Flask-приложению
#from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__) #Создаем переменную app, в которой будет Flask приложением, куда передаем __name__ имя текущего файла для инициализации.
    app.config.from_pyfile('config.py')
    db.init_app(app)

    #Flask использует пути, надо привязать функцию обработчик к какому-то пути на сайте
    @app.route('/') #Декоратор позволяет функции открываться, когда пользователь зайдет на главную страницу сайта

    def index(): #Функция возвращает текст, который нужно вывести на сайте
        title = "Жизнь Python"
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        #weather = False  #Если дать такое значение, выйдет "Сервис погоды временно недоступен". Причем при запущенном файле все обновится автоматом и выдаст на сайте.
        news_list = News.query.order_by(News.published.desc()).all()
        #Теперь этот код не нужен, когда в index.html прописали  Погода: {{weather.temp_C }}, ощущается как {{weather.FeelsLikeC }}
        """if weather : #Проверяем, что weather действительно вернулся, а не False.
            weather_text =  f"Погода: {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}" #Надо вставить внутрь строки часть данных, которые пролучили в weather.
        else :
            weather_text = "Сервис погоды временно недоступен" """
        
        
        return render_template('index.html', page_title = title, weather12 = weather, news_list = news_list)

    return app