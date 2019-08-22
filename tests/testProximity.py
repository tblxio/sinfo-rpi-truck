from proximityClass import ProximitySensor
import unittest2
import time


class TestGpio(unittest2.TestCase):

    def setUp(self):
        self.proximity = ProximitySensor("test")
        self.proximity.setup(0.4)

    def testMeasurementExists(self):
        """
        Test that it can access the GPIO and take a measurement
        """
        for _ in range(4):
            print self.proximity.measureDistance()
            time.sleep(0.2)
        self.assertGreater(self.proximity.measureDistance(), 0)


if __name__ == '__main__':
    unittest2.main()
