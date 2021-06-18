import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import math
import operator
import os
import extractor

"""Sensor setup
# This library supports several Inertial Measurement Units (IMU's) and allow
# us to easily communicate with the sensor
"""
# Load configuration file: sensor settigs + calibration
SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

t_shutdown = 0
if (not imu.IMUInit()):
    print("IMU Init Failed, try #: ".format(str(t_shutdown)))
    t_shutdown += 1
    if t_shutdown > 9:
        sys.exit(1)

else:
    print("IMU Init Succeeded")

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

poll_interval = imu.IMUGetPollInterval()

mapping = {
    "udp": extractor.loop_udp,
    "tcp": extractor.loop_tcp,
    "log": extractor.loop_log,
    "producer": extractor.loop_producer
}

fields = ["accel", "gyro", "timestamp"]
mapping[sys.argv[1]](imu, poll_interval, fields)
