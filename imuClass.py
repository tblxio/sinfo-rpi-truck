from componentClass import Component
import time
import os.path
import operator
import RTIMU
import os
import sys
import getopt
import json
sys.path.append('.')


class Imu(Component):
    """
    An implementation of the component class to acquire and publish the 
    data from the Inertial Measurement unit, namely the data from the
    accelerometer and the gyroscope.
    """

    # Setup method for this specific device
    def setup(self):
        # This is mostly the legacy code used in the SINFO Workshop
        # Load configuration file: sensor settigs + calibration
        SETTINGS_FILE = "RTIMULib"
        self.s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)
        self.counter =0
        self.timer = time.time()
        print("IMU Name: " + self.imu.IMUName())

        t_shutdown = 0
        if (not self.imu.IMUInit()):
            print ("IMU Init Failed, try #: ".format(str(t_shutdown)))
            t_shutdown += 1
            if t_shutdown > 9:
                sys.exit(1)

        else:
            print "IMU Init Succeeded"

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        # Used to set up the polling interval of the sensor
        # Converted from mS to seconds
        # (400/self.imu.IMUGetPollInterval()) gives the sampling rate in Hz.
        # We multiply by 2 in order to be slower than the sampling rate and
        # guarantee a hit everytime we try to read the sensor
        # In this case the sampling rate is 100Hz and we are sampling every 
        # 2/100Hz= 20ms
        self.sampInterval = 1.0/(400/self.imu.IMUGetPollInterval())*2*10
        self.set_topic("imu")

        print "{} setup finished".format(self.name)

    # Data Handling for this specific device, from collection to 
    # publishing to the correct MQTT Topics.
    def handleData(self, timestamp):
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            self.mqttHandler.publish(self.my_topic, json.dumps(self.gen_payload_message(data,timestamp)),retain=True)
            self.counter+=1
            elapsed = time.time() - self.timer
            self.timer = time.time()
            print "{} : time elapsed {}".format(self.counter,elapsed)
        else:
            print "ops"

    # Generates the payload specific to the IMU
    def gen_payload_message(self, data,timestamp):
        try:
            payload = {
                'accel': {
                    'x': data.get('accel')[0],
                    'y': data.get('accel')[1],
                    'z': data.get('accel')[2]
                },
                'gyro': {
                    'x': data.get('gyro')[0],
                    'y': data.get('gyro')[1],
                    'z': data.get('gyro')[2]
                },
                # Note: This is a UNIX timestamp in microseconds
                #'timestamp': data.get('timestamp')

                'timestamp': timestamp
            }
        except: 
            print("Received wrong data structure")
        return payload

