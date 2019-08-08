import unittest
import time
import sys
sys.path.append('..')
from imuClass import Imu


class TestImu(unittest.TestCase):

    def setUp(self):
        self.imu= Imu("test")
        self.imu.setup()

    def testImuGetData(self):
        """
        Test that it can take a measurement
        """
        while True:
            if self.imu.imu.IMURead():
                data = self.imu.imu.getIMUData()
                self.assertIsNotNone(data)
                break
        time.sleep(0.1)

    def testImuHandleData(self):
        """
        Test that it can publish the measurement to the Mqtt Broker
        """
        self.imu.handleData(time.time())
        
if __name__ == '__main__':
    unittest.main()