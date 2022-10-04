from flask import current_app #Образаемся к текущему flask-приложению
import requests         #Библиотека requests посылает запрос определенного типа к серверу и возвращает результат.

def weather_by_city(city_name):         #Функция должна принимать название города, для которого запрашиваем погоду
    weather_url = "current_app.config['WEATHER_URL']"
    params = {
        "key" : current_app.config['WEATHER_API_KEY'],
        "q" : city_name,
        "format" : "json",
        "num_of_days" : 1,
        "lang" : "ru"
    }
    try:                #Если инет включен, идем по этому пути
        result = requests.get(weather_url, params = params)         #Библиотека requests сходит на URL на сайт, возьмет данные и вренет нам.
        result.raise_for_status()            #Этот вызов сгенерирует исключение, если сервер ответил кодом, начинающимся с 4xx или 5xx
        weather = result.json()             #Преобразование полученных данных из строки в стандартные для Питона форматы (словарь, список)
        """if работает так: либо он возвращает словарь(current_condition) в списке успешно, либо он возвращает False, если ни один из return не прошел"""
        if 'data' in weather:                #Проверяем секцию дата в погоде
            if 'current_condition' in weather['data']:      #Проверяем внутри даты текущую погоду
                try:                        #Если есть и дата и текущая погода(у нас список), надо вернуть первый словарь в списке. Список может быть пустым, поэтому try-except.
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
    except (requests.RequestException, ValueError):         #Этим except перехватываем ошибку об отключенном инете.
        print("Сетевая ошибка")
        return False
    return False

if __name__ == "__main__":      #Блок отработает, если вызываем напрямую типа "Python weather.py", если из сервера - то не отработает. как и нужно
    w = weather_by_city("Sochi, Russia")
    print(w)        #Когда есть return (возвращение значения), то значение надо куда-то положить (print)