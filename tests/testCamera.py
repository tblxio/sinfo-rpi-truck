from cameraClass import Camera
import unittest2
import sys
sys.path.append('..')


class TestCamera(unittest2.TestCase):

    def setUp(self):
        self.camera = Camera("test")
        self.camera.setup()

    def testCameraInfoRequest(self):
        """
        Test that it can publish the feed to the Mqtt Broker
        and start streaming
        """
        self.camera.run()

if __name__ == '__main__':
    unittest2.main()
