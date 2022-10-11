from flask import Blueprint, current_app, render_template

from webapp.news.models import News
from webapp.weather import weather_by_city

blueprint = Blueprint('news', __name__)

@blueprint.route('/') #Декоратор позволяет функции открываться, когда пользователь зайдет на главную страницу сайта
def index(): #Функция возвращает текст, который нужно вывести на сайте
    title = "Жизнь Python"
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    #weather = False  #Если дать такое значение, выйдет "Сервис погоды временно недоступен". Причем при запущенном файле все обновится автоматом и выдаст на сайте.
    news_list = News.query.order_by(News.published.desc()).all() #Верни все новости из БД. order_by(News.published.desc - сортировка по дате от большего к меньшему
    return render_template('news/index.html', page_title = title, weather12 = weather, news_list = news_list)