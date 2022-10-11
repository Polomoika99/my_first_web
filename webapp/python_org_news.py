from datetime import datetime

import requests
from bs4 import BeautifulSoup

from webapp.db import db, News
from webapp.news.models import News

def get_html(url):
    try:
        result = requests.get(url) #При помощи requests берем данные из url
        result.raise_for_status() #Эта функция дает воз-ть не выводить 404, а обрабатывать исключение и возвращать какое-то значение
        return result.text
    except(requests.RequestExceptione, ValueError): #RequestExceptione - если сетевая проблема, ValueError - если сетевая проблема
        print("Сетевая ошибка")
        return False

def get_python_news():
    html = get_html("https://www.python.org/blogs/") #https://www.python.org/blogs/ - адрес, который собираем
    if html:
        soup = BeautifulSoup(html, 'html.parser') #soup - преобразованный html. Берем дерево элементов, которое принимает html и указываем парсер.
        all_news = soup.find('ul', class_='list-recent-posts')
        all_news = all_news.findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text #Вот эта 'a' решает. В "простыне" через нее отыскивается и выводится текст. 
            """<h3 class="event-title"><a href="http://pyfound.blogspot.com/2022/07/distinguished-service-award-granted-to.html">
            Distinguished Service Award Granted to Naomi Ceder</a></h3><p><time datetime="2022-07-21">July 21, 2022</time></p>
            Вышло: Distinguished Service Award Granted to Naomi Ceder"""
            url = news.find('a')['href'] #К атрибутам обращаемся как к элементам словаря. Вытаскивает ссылку: href="http://pyfound.blogspot.com/2022/07/distinguished-service-award-granted-to.html
            published = news.find('time').text
            try:
                published = datetime.strptime(published, "%Y-%m-%d") #Убедились, что в поле published действительно лежит дата.
            except(ValueError):
                published = datetime.now()
            save_news(title, url, published)
            

def save_news(title, url, published): #Добавим функцию для записи новости в БД
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        new_news = News(title=title, url = url, published = published) #Создали объект класса News
        db.session.add(new_news) #Положили объект в сессию Алхимии
        db.session.commit() #Новость сохранена в БД








#result_news.append({
                #"title": title,
                #"url": url,
                #"published": published
            #})
            #print(title)
            #print(url)
            #print(published)
        #return result_news #result_news - список словарей, который содержит title, url, published
    #return False

#if __name__ == "__main__":
    #html = get_html("https://www.python.org/blogs/") #https://www.python.org/blogs/ - адрес, который собираем
    #if html:
        #with open("python.org.html", "w", encoding="utf8") as f:
        #    f.write(html)
       # news = get_python_news(html)
        #print(news)
