import paho.mqtt.client as mqtt
from config import configuration as config


class MqttClient(mqtt.Client):
    """
    Extends the normal mqttClient class to implement some connection parameters
    that should be generic to all the components in the system
    """

    # The callback for when the client receives a CONNACK
    # response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    # The callback for disconnection, which stops the loop()
    def on_disconnect(self, client, userdata, rc=0):
        print("Disconnected result code " + str(rc))
        self.loop_stop()

    # Sets up the connection with the broker on the server specified
    #  in mqttconfig.py
    def setup_client(self):
        self.username_pw_set(config.mqttUser, password=config.mqttPasswd)
        self.connect(config.mqttBroker, config.mqttPort, 60)
        self.loop_start()
