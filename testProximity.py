import unittest
import time
import proximityClass
from proximityClass import ProximitySensor


class TestGpio(unittest.TestCase):
    
    def setUp(self):
        self.proximity= ProximitySensor("test")
        self.proximity.setup()
    
    def testMeasurementExists(self):
        """
        Test that it can access the GPIO and take a measurement
        """
        for i in range(4):
            print self.proximity.measureDistance()
            time.sleep(2)
        self.assertGreater(self.proximity.measureDistance(),0)

    def testMqttPublish(self):
        """
        Test that it can publish the measurement to the Mqtt Broker
        """
        self.proximity.handleData(time.time())
        
if __name__ == '__main__':
    unittest.main()