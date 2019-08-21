from componentClass import Component
from subprocess import call
import socket
import time
import json
import os


class Camera(Component):

    def setup(self):
        self.sampInterval = 100.0
        self.set_topic("camera")
        self.path = os.path.dirname(
            os.path.abspath(__file__)) + "/config/cameraRunner.py"
        print self.path
        print "{} setup finished".format(self.name)

    # Basically publishes the camera feed IP to the MQTT broker
    # and calls the cameraRunner, which is based on a python3 script,
    # therefore i couldn't include here, since the rest of the project
    # is built using python 2.7. It should be changed in the future
    # as it was done as a hackish solution.
    def run(self):
        self.mqttHandler.publish(self.my_topic, json.dumps(
            self.gen_payload_message(round(time.time() * 1000))), retain=True)
        time.sleep(3)
        call(["sudo", "-u", "pi", "python3", self.path])

    def gen_payload_message(self, timestamp):
        return {
            'stream_ip': self.get_ip_address(),
            'stream_port': "8000",
            'timestamp': timestamp
        }

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
