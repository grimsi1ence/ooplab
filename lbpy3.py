class Calling:
    def calling(self):
        return "make call"
class SMS:
    def send_sms(self):
        return "send sms"
class NetworkConnection:
    def net_connection(self):
        return "connection to network"
class TelecomDevice(NetworkConnection):
    def working_telecomdevice(self):
        return self.net_connection()
class IoTDevice(SMS):
    def send_data(self):
        return f"from MCU: {self.send_sms()}"

iot=IoTDevice().send_data()
print(iot)