"""Template of URL to insert values in"""
from api.open_weather.config import API_KEY

URL_TEMPLATE = ('http://api.openweathermap.org/data/2.5/weather?'
                'q={city}&units=metric&lang=ru&'
                f'appid={API_KEY}')
