import unittest
import time
import sys
sys.path.append('..')
from cameraClass import Camera


class TestCamera(unittest.TestCase):

    def setUp(self):
        self.camera= Camera("test")
        self.camera.setup()

    def testCameraInfoRequest(self):
        """
        Test that it can publish the measurement to the Mqtt Broker
        """
        self.camera.run()
        
if __name__ == '__main__':
    unittest.main()