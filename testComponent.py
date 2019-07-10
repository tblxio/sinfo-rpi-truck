from componentClass import Component
import time
import os.path
import operator
import RTIMU
import os
import sys
import getopt
import json
sys.path.append('.')


class TC(Component):
    """
    An implementation of the component used to test the multi threading
    functionallity of the main.py. It's similar to the ImuClass, but with
    dummy data
    """

    # Setup method for this specific device
    def setup(self):
        print("Started test")
        # Used to set up the polling interval of the sensor
        self.poll_interval = 10
        self.my_topic = "truck1/test"

    # Data Handling for this specific device, from collection to publishing to the correct MQTT Topics.
    def handleData(self):
        data = {"accel": (0, 1, 2), "gyro": (0, 1, 2), "timestamp": 123445}
        self.mqttHandler.publish(self.my_topic, json.dumps(
            self.gen_payload_message(data)))

    # Specific run behaviour of this component
    def run(self):
        self.setup()
        self.mqttHandler.publish(
            (self.my_topic+"/pollRate"), self.poll_interval*1.0/1000.0, retain=True)
        while True:
            self.handleData()
            time.sleep(self.poll_interval*1.0/1000.0)

    def gen_payload_message(self, data):
        try:
            payload = {
                'accel': {
                    'x': data.get('accel')[0],
                    'y': data.get('accel')[1],
                    'z': data.get('accel')[2]
                },
                'gyro': {
                    'x': data.get('gyro')[0],
                    'y': data.get('gyro')[1],
                    'z': data.get('gyro')[2]
                },
                'timestamp': data.get('timestamp')
            }
        except:
            print("Received wrong data structure")
        return payload
