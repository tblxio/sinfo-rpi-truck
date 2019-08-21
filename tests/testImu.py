import unittest2
import time
from imuClass import Imu


class TestImu(unittest2.TestCase):

    def setUp(self):
        self.imu = Imu("test")
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


if __name__ == '__main__':
    unittest2.main()
