import requests
from .json_base import JsonOperations


class RestWeatherClient:
    def __init__(self, API_key):
        self.API_key=API_key
    def get_lat_lon(self, city, country_code):
        endpoint_for_get_lat_lon=f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&appid={self.API_key}"
        res=requests.get(endpoint_for_get_lat_lon)
        r=res.json()
        if res.status_code==200:
            inf=r[0]
            lat=inf['lat']
            lon=inf['lon']
            return lat,lon
        else:
            print(res.status_code)
    def get_weather(self, coordinates: tuple):
        weather_endpoint=f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={self.API_key}&units=metric"
        res=requests.get(weather_endpoint)
        if res.status_code==200:
            r=res.json()
            return r
        else:
            print(f"code: {res.status_code}")
class Weather:
    def __init__(self):
        self.info={}
    def basic_weather_info(self, full_weather):
        main=full_weather['main']
        wind=full_weather['wind']
        self.info.update({'temp': main['temp']})
        self.info.update({'pressure': main['pressure']})
        self.info.update({'humidity': main['humidity']})
        self.info.update({'wind speed': wind['speed']})
        return self.info
    @staticmethod
    def return_temp(weather):
        if 'temp' not in weather:
            return "empty dict"
        else:
            return f"temp: {weather['temp']}°C"
class RestClient:
    def __init__(self, url):
        self.url=url
    def get(self, resource):
        endpoint=f"{self.url}/{resource}"
        res=requests.get(endpoint)
        if res.status_code==200:
            data=res.json()
            print('OK')
            return data
        else:
            print(f'error: {res.status_code}')
    def post(self, resource, data):
        endpoint=f"{self.url}/{resource}"
        res=requests.post(endpoint, json=data)
        if res.status_code==201:
            print("created post", res.json())
        else:
            print(f"{res.status_code}")
    def delete(self, resourse, number_post):
        endpoint=f"{self.url}/{resourse}/{number_post}"
        res=requests.delete(endpoint)
        if res.status_code==200 or res.status_code==204:
            print(f'post deleted')
        else:
            print(f"error: {res.status_code}")
    def put(self, resourse, number_post, new_data):
        endpoint=f"{self.url}/{resourse}/{number_post}"
        res=requests.put(endpoint, json=new_data)
        if res.status_code==200 or res.status_code==204:
            print(f'post updated')
        else:
            print(f"error: {res.status_code}")
