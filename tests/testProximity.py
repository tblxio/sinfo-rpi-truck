import unittest
import time
sys.path.append('..')
from proximity import ProximitySensor


class TestGpio(unittest.TestCase):
    
    def setUp(self):
        self.proximity= ProximitySensor("test")
        self.proximity.setup()
    
    def testMeasurementExists(self):
        """
        Test that it can access the GPIO and take a measurement
        """
        self.assertGreater(self.proximity.measureDistance(),0)
        self.assertGreater(4,self.proximity.measureDistance())

    def testMqttPublish(self):
        """
        Test that it can publish the measurement to the Mqtt Broker
        """
        self.proximity.handleData(time.time())
        
if __name__ == '__main__':
    unittest.main()