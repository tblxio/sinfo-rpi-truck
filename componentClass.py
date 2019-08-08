from mqttClient import MqttClient
from abc import ABCMeta, abstractmethod
import sys,signal
import json
import math 

class Component:

    __metaclass__ = ABCMeta

    def __init__(self,root):
        self.mqttHandler = MqttClient()
        self.mqttHandler.setup_client()

        self.name= "component"
        self.sampInterval = 1
        self.loopCycles = 1
        self.loopRate = 1
        self.rootTopic = root
        self.config_topic = self.rootTopic + "/components/" + self.name
        self.my_topic = self.rootTopic + "/" + self.name

        
    # Component specific setup 
    # Needs to contain all the code to be executed once 
    # before the loop starts
    # Needs to be implemented in order for the main to run correctly
    @abstractmethod
    def setup(self):
        pass


    # Component specific data handling and MQTT publishing 
    # It should receive the main timestamp to stamp the package
    # in order to ensure coherence between components.
    #
    # Needs to be implemented in order for the main to run correctly
    def handleData(self,timestamp):
        pass
    

    # Run code for components which are suposed to loop in paralel
    # and do not require data acquisition, such as the camera
    def run(self):
        pass


    # Component specific setup JSON payload generation
    # (Good practice to implement it, so it's well organized)
    def gen_payload_message(self, data,timestamp):
        pass


    # Calculate the number of loop cycles before sampling the 
    # sensor based on the rate the loop is run and publish
    # the new configuration parameters of the component
    def calculate_loop_cycles(self,loop_rate,timestamp):
        self.loopRate = loop_rate
        self.loopCycles = int(math.ceil(self.sampInterval / self.loopRate))
        self.publishConfiguration(int(timestamp))


    # Publish component configuration values to the
    # root/component/config topic
    def publishConfiguration(self,timestamp):
        self.mqttHandler.publish(self.config_topic, json.dumps(
            self.gen_curr_configuration_message(timestamp)), retain=True)
    

    # Generate current configuration message
    def gen_curr_configuration_message(self,timestamp):
       return {
           'name': self.name,
           'topic': self.my_topic,
           'pollRate': self.sampInterval,
           'loopRate': self.loopRate,
           'cycles': self.loopCycles,
           'timestamp': timestamp
       }
    
    # Set component topic
    def set_topic(self,component_name):
        self.name=component_name
        self.my_topic = self.rootTopic + "/" + self.name