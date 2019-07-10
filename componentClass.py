from mqttClient import MqttClient
from abc import ABCMeta, abstractmethod
import sys,signal


class Component:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.mqttHandler = MqttClient()
        self.mqttHandler.setup_client()
        
    # Component specific setup 
    # (Good practice to implement it, so it's well organized)
    def setup(self):
        pass

    # Component specific data handling and MQTT publishing 
    # (Good practice to implement it,so it's well organized)
    def handleData(self):
        pass

    # Component specific run code 
    # Needs to be implemented so the main.py can work correctly
    @abstractmethod
    def run(self):
        pass
