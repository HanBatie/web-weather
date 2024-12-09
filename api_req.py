# импорт необходимых библиотек
import requests
import pandas as pd
import json
from api_key import API_KEY

api_key = API_KEY

class Weather:

    def __init__(self, api_key):
        self.api_key = api_key
        self.loc_key = None
        self.cached_data = None

    # функция получения погоды по координатам
    def get_loc_key_by_coords(self, lat, lon):
        #получение location key
        loc_key_url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={self.api_key}&q={lat},{lon}'
        r = requests.get(loc_key_url)
        if r.status_code == 200:
            self.loc_key = r.json()['Key']
        else:
            print(f"Ошибка {r.status_code}, при запросе location_key")
            return None

    def get_weather_data(self):
        #Получение данных о погоде, по location key
        weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{self.loc_key}?apikey={self.api_key}&language=ru&details=true&metric=true'
        r = requests.get(weather_url)
        if r.status_code == 200:
            weather_data = r.json()
        else:
            print(f"Ошибка {r.status_code}, при получении погодных условий")
            return None

        #Извлечение ключевых параметров
        temperature = weather_data[0]['Temperature']['Metric']['Value']
        humidity = weather_data[0]['RelativeHumidity']
        wind_speed = weather_data[0]['Wind']['Speed']['Metric']['Value']
        if not(weather_data[0]['HasPrecipitation']):
            daily_forecasts_url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{self.api_key}?apikey={self.api_key}&language=ru&details=true&metric=true'
            r = requests.get(daily_forecasts_url)
            if r.status_code == 200:
                forecasts = r.json()
                prob_day = forecasts['DailyForecasts'][0]['Day']['RainProbability']
                prob_night = forecasts['DailyForecasts'][0]['Night']['RainProbability']
                rain_prob = ((prob_day+prob_night) - prob_night*prob_day)*100
            else:
                return (f'Не удалось получить данные о вероятности дожджя, ошибка {r.status_code}')
        else:
            rain_prob = 100

        #сохранение параметров
        self.cached_data = {'Температура(C)': temperature,
                  'Влажность(%)': humidity,
                  'Скорость ветра': wind_speed,
                  "Вероятность дождя(%)":rain_prob}

        return self.cached_data

