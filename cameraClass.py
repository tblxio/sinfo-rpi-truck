from componentClass import Component
from subprocess import call
import socket
import time
import json

class Camera(Component):

    def setup(self):
        self.sampInterval = 100
        self.set_topic("camera")
        print "{} setup finished".format(self.name)

    def run(self):
        self.mqttHandler.publish(self.my_topic, json.dumps(
            self.gen_payload_message(time.time())), retain=True)
        call(["python3", "config/cameraRunner.py" ])

    def gen_payload_message(self,timestamp):
        return {
                'stream_ip': self.get_ip_address(),
                'stream_port': 8000,
                'timestamp': timestamp
            }

    def get_ip_address(self):
        ip_address = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address