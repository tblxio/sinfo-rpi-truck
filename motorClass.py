from componentClass import Component
import json


class Motor(Component):
    """
    An implementation of the component used to request data from the
    motor periodically, which then sends it to the corresponding topic
    to be read by the API
    """

    # Setup method for this specific device
    def setup(self):
        self.sampInterval = 10.0
        self.requestTopic = "sbrick/01/rr/get_adc"
        self.set_topic("motor")
        print "{} setup finished".format(self.name)

    # Data Handling for this specific device, from collection to publishing to
    # the correct MQTT Topics.
    def handleData(self, timestamp):
        self.mqttHandler.publish(self.requestTopic, json.dumps(
            self.gen_request_message(timestamp)), retain=True)

    def gen_request_message(self, timestamp):
        return {'status': 0, 'req_msg': '{"sbrick_id": "88:6B:0F:80:29:D1"}',
                'resp_topic': self.my_topic, 'timestamp': timestamp}
