import requests
import json

class JsonOperations:
    def __init__(self, filename: str):
        self.filename=filename
    def save_to_json(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
    def read_json(self):
        with open(self.filename, 'r') as f:
            read_data=json.load(f)
            return read_data
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
    
API_key='64500f1902a39a8c1850388c51575fbd'
Ukraine_code=804
UK_code=826

rest_client=RestWeatherClient(API_key)

coordinates=rest_client.get_lat_lon('Lviv', Ukraine_code)
weather_dict=rest_client.get_weather(coordinates)

coordinates_London=rest_client.get_lat_lon('London', UK_code)
weather_dict_London=rest_client.get_weather(coordinates_London)

weather_London_json=JsonOperations('weather_London.json')
weather_London_json.save_to_json(weather_dict_London)

base_info_London=weather_London_json.read_json()
weather_london=Weather().basic_weather_info(base_info_London)

json_base_info_london=JsonOperations('base_weather_London.json')
json_base_info_london.save_to_json(weather_london)

file_json=JsonOperations('weather_Lviv.json')
file_json.save_to_json(weather_dict)
base_info_lviv=file_json.read_json()

weather_base=Weather().basic_weather_info(base_info_lviv)

json_base_info=JsonOperations('base_weather_Lviv.json')
json_base_info.save_to_json(weather_base)