import paho.mqtt.client as mqtt
import time

class MQTTclient:
    def __init__(self, broker_address, broker_port, username, password):
        self.client=mqtt.Client()
        self.broker_address=broker_address
        self.broker_port=broker_port
        self.client.tls_set()
        self.client.username_pw_set(username, password)
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Підключено до MQTT брокера")
        else:
            print(f"Помилка підключення, код: {rc}")
    def on_publish(self, client, userdata, mid):
        print(f"Повідомлення успішно опубліковано (mid={mid})")
    def on_disconnect(self, client, userdata, rc):
        print("Відключено від MQTT брокера")
    def subscribe(self, topic):
        self.client.subscribe(topic)
        print(f"Підписано на тему '{topic}'")
    def on_message(self, client, userdata, msg):
        print(f"Отримано повідомлення з '{msg.topic}': {msg.payload.decode()}")
    def callback(self):
        self.client.on_connect=self.on_connect
        self.client.on_publish=self.on_publish
        self.client.on_message=self.on_message
        self.client.on_disconnect=self.on_disconnect
    def connect(self):
        time.sleep(1)
        self.client.connect(self.broker_address, self.broker_port)
        print(f"підключено до брокера: {self.broker_address}")
    def publish(self, topic, message):
        time.sleep(1)
        result=self.client.publish(topic, message)
        result.wait_for_publish()
        print(f"Опубліковано в тему '{topic}': {message}")
    def disconnect(self):
        time.sleep(1)
        self.client.disconnect()
        self.client.loop_stop()