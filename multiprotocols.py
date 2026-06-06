from protocols import mqtt_client, websocket
from protocols.RESTclient import RestWeatherClient, Weather
import asynciо
API_key='64500f1902a39a8c1850388c51575fbd'
Ukraine_code=804
CITY="Lviv"

WS_URI="wss://ws.postman-echo.com/raw"

BROKER_ADDRESS = "f8330c6687b54a7b9b0155a17805a778.s1.eu.hivemq.cloud"
BROKER_PORT = 8883
TOPIC1 = "temperature from OpenWeather"
USERNAME="hivemq.webclient.1774016733348"
PASSWORD="p2@9;X&Mr%b8n1LjOFAg"

class WeatherMultiprotocol:
    def __init__(self):
        try:
            self.rest_client = RestWeatherClient(API_key)
            self.ws_client = websocket.Websocket(WS_URI)
            self.mqtt_client = mqtt_client.MQTTclient(BROKER_ADDRESS, BROKER_PORT, USERNAME, PASSWORD)
        except Exception as e:
            print(f"Помилка при ініціалізації клієнтів: {e}")
            self.rest_client = None
            self.ws_client = None
            self.mqtt_client = None
    def rest_get(self):
        map_location=self.rest_client.get_lat_lon(CITY, Ukraine_code)
        full_weather=self.rest_client.get_weather(map_location)
        weather=Weather()
        basic_weather=weather.basic_weather_info(full_weather)
        result=weather.return_temp(basic_weather)
        return result
    async def ws_send(self, result):
        await self.ws_client.connect()
        await self.ws_client.send(result)
        await self.ws_client.close()
    async def ws_receive(self):
        return await self.ws_client.rx()
    def mqtt_publish(self, topic, msg):
        self.mqtt_client.callback()
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(topic)
        self.mqtt_client.publish(topic, msg)
        self.mqtt_client.disconnect()

multiprotocol=WeatherMultiprotocol()
get=multiprotocol.rest_get()
asyncio.run(multiprotocol.ws_send(get))
data_from_ws=asyncio.run(multiprotocol.ws_receive())
multiprotocol.mqtt_publish(TOPIC1, data_from_ws)
