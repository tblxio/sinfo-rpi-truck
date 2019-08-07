import unittest
import time
sys.path.append('..')
from motorClass import Motor


class TestMotor(unittest.TestCase):

    def setUp(self):
        self.motor= Motor("test")
        self.motor.setup()

    def testMotorInfoRequest(self):
        """
        Test that it can publish the measurement to the Mqtt Broker
        """
        self.motor.handleData(time.time())
        
if __name__ == '__main__':
    unittest.main()