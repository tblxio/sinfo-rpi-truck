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
        # Used to set up the polling interval of the sensor
        self.poll_interval = 0.12
        self.my_topic = "truck1/testcomponent"
        self.name = "testcomponent"
        print "{} setup finished".format(self.name)

    # Data Handling for this specific device, from collection to publishing to the correct MQTT Topics.
    def handleData(self,timestamp):
        data = {"accel": (0, 1, 2), "gyro": (0, 1, 2), "timestamp": 123445}
        self.mqttHandler.publish(self.my_topic, json.dumps(
            self.gen_payload_message(data,timestamp)), retain=True)

    def gen_payload_message(self, data,timestamp):
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
                'timestamp': timestamp
            }
        except:
            print("Received wrong data structure")
        return payload
