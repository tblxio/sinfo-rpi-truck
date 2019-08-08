import RPi.GPIO as GPIO
import os
import sys
import getopt
import json
from componentClass import Component
import time
import os.path

class ProximitySensor(Component):
    """
    An implementation of the component used to request data from the
    motor periodically, which then sends it to the corresponding topic
    to be read by the API
    """

    # Setup method for this specific device
    def setup(self):
        self.sampInterval = 0.3
        self.set_topic("proximity")

        # Setup the GPIO pins
        self.TRIG = 17
        self.ECHO = 27
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG,GPIO.OUT)
        GPIO.setup(self.ECHO,GPIO.IN)
        GPIO.output(self.TRIG, False)
        GPIO.setwarnings(False)
        time.sleep(1)
        self.filtered_distance = [0]*10
        print "{} setup finished".format(self.name)

    # Data Handling for this specific device, from collection to publishing to the correct MQTT Topics.
    def handleData(self,timestamp):
        self.mqttHandler.publish(self.my_topic, json.dumps(
            self.gen_payload_message(self.measureDistance(),timestamp)), retain=True)

     # Generates the payload specific to the IMU
    def gen_payload_message(self, distance,timestamp):
        return {
                'distance': distance,
                'timestamp': timestamp
            }

    def measureDistance(self):
        # Trigger the sensor
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        pulse_start=0
        pulse_end=0

        # Wait for Sonar Response
        begin = time.time()
        while GPIO.input(self.ECHO)==0:
            pulse_start = time.time()
            if (pulse_start - begin) > 0.01:
                begin = 1
                break
        if begin ==1:
            return self.filtered_distance

        else:
            while GPIO.input(self.ECHO)==1:
                pulse_end = time.time()      

        # Get the duration of the pulsem which indicates the time
        # it took for the sound wave to come back
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150.0
        if distance < 4:
            distance =4
        # Calculate the distance in cm based on the speed of sound/2
        del self.filtered_distance[0]
        self.filtered_distance.append(distance)
        # Round to 2 decimal points
        return round(sum(self.filtered_distance)/10, 2)
    





