# Introduction

This repo describes the set up of the raspberry pi that is later used along with the Mercedes-Benz Arocs (Lego truck) to stream gyro and accelerometer data.

# Connect the cables and stream sensor data
### Requirements:
- MPU-9250;
- Micro SD card + Adaptor to connect to your laptop;
- Raspberry Pi 3 Model B+ (RPi) + Charger;
- Keyboard + mouse + screen;
- Jumper wires to connect sensor to RPi (some other options are available);

The sources that were used to set up the RPi were mainly:
- https://kingtidesailing.blogspot.com/2016/02/how-to-setup-mpu-9250-on-raspberry-pi_25.html
- https://github.com/richardstechnotes/RTIMULib2

So it is expected that most of the instructions will be similar to the ones you can find there.

### Step 1: OS setup on RPi

In order to setup your RPi follow the instructions [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3).
In the end you should have your RPi up and running with its own OS.


### Step 2: Connect the cables

The sensor will have the GND, VCC, SDA and SCL pins connected to the RPi. Here you need to be careful to connect the VCC to the right pin in the RPi otherwise you can damage it. So, following the diagram

![RPi diagram](/j8header-2b-large.png)

You should connect:

| Raspberry Pi (RPi) | Sensor MPU-9250 |
| ------ | ------ |
| 3.3 VDC Power - 1 | VCC |
| GPIO 8 SDA1 (I2C) - 3 | SDA |
| GPIO 9 SCL1 (I2C) - 5 | SCL |
| Ground - 9 | GND |

### Step 3: Install libraries and connect the sensor

Create and cd into the folder where the whole project will sit (and create a scripts folder that will be used later as our working directory):
```sh
$ mkdir truck_project_db
$ cd truck_project_db
$ mkdir scripts
```

Then install the I2C software
```sh
$ sudo apt-get install i2c-tools
```

In the Menu (top left corner) go to Preferences > Raspberry Pi Configuration > Interfaces and enable i2c. This last step requires a reboot.
```sh
$ sudo reboot
```

Verify if the sensor is connected by running
```sh
$ sudo i2cdetect -y 1
```
the number 68 should show up in the grid, corresponding to the sensor's default address.

The following installations are needed:
```sh
$ sudo apt-get install cmake
$ sudo apt-get install python-dev
$ sudo apt-get install octave
```

If you get an error related with jre-headless run the following:
```sh
$ sudo apt-get purge openjdk-8-jre-headless
$ sudo apt-get install openjdk-8-jre-headless
$ sudo apt-get install openjdk-8-jre
```

Next clone the repository that has the tools to interface with the sensor:
```sh
$ git clone https://github.com/richardstechnotes/RTIMULib2.git
```

This repository contains several different apps that might be worth exploring. In our case we are going to install only the app that will help us to calibrate the sensor:
```sh
$ cd RTIMULib2/Linux/RTIMULibCal
$ make -j4
$ sudo make install
```

Then we need to copy `RTEllipsoidFit` folder into a folder that is at the same level as our working directory (requirement stated in the `RTIMULib` repo) - in our case `scripts` folder:
```sh
$ cp -r /home/pi/kts/RTIMULib2/RTEllipsoidFit/ /home/pi/kts/
$ cd /home/pi/kts/RTEllipsoidFit/
```
Follows some edits stated in the `RTIMULib`'s repo before we can proceed to calibrate our sensor.

- edit file `/etc/modules`
    ```sh
    $ sudo vi /etc/modules
    ```
    this file should contain the following lines uncommented / added:

    	i2c-dev
    	i2c-bcm2708

- edit/create file `/etc/udev/rules.d/90-i2c.rules`:
    ```sh
    $ sudo vi /etc/udev/rules.d/90-i2c.rules
    ```
    add the following line to the file:

        KERNEL==“i2c-[0-7]”,MODE=“0666” in /etc/udev/rules.d/90-i2c.rules


- edit/create file `/boot/config.txt`:
    ```sh
    $ sudo vi /boot/config.txt
    ```

    and add at the bottom of the file the line

        dtparam=i2c1_baudrate=400000

After all the edits reboot your RPi:
```sh
$ sudo reboot
```

### Step 4: Calibrating MPU-9250

From `/home/pi/truck_project_db/RTEllipsoidFit/` run
```sh
$ RTIMULibCal
```

and follow the instructions to calibrate the sensor. Then copy the file resulting from the calibration `RTIMULib.ini` to the working directory:
```sh
$ cp RTIMULib.ini /home/pi/truck_project_db/scripts
```

in order to change the sampling rate it is advised to do so in the file `RTIMULib.ini`. In this particular example we tuned the following parameters:
```
MPU9250GyroAccelSampleRate=5
MPU9250CompassSampleRate=5
MPU9250GyroLpf=2
MPU9250AccelLpf=2
```


### Step 5: Visualizing the sensor (optional)
In order to evaluate if the calibration process went well we will use a visualization tool `RTIMULibDemoGL` that will read the sensor data and show the axis orientation in real-time. In order to setup the RTIMULibDemoGL app you need to install the following:
```sh
$ sudo apt-get install cmake
$ sudo apt-get install libqt4-dev
```

Then we can proceed with the instalation of the app:
```sh
$ cd /home/pi/truck_project_db/RTIMULib2/Linux/RTIMULibDemoGL
$ qmake
$ make -j4
$ sudo make install
```

Now if you want to try out and visualize your sensor working run
```sh
$ RTIMULibDemoGL
```

Other apps are available in `/RTIMULib2/Linux/`. Check out its repo for description of the apps and how to set them up.

### Step 6: Streaming script

In this repo you will find the file imu.py that will stream the sensor data. This script allows you to get data in three modes. Every 100th sensor read we print it to the console just for sanity check.

#### Mode: PRODUCER

`python imu.py producer` : This is the mode we are using in the workshop. In this case it runs a kafka producer and the sensor signals are sent to a kafka broker that can later be consumed by a kafka consumer.

The consumer is set up [here](https://github.com/TechhubLisbon/sinfo-frontend).

#### Mode: UDP

`python imu.py udp` : UDP/SOCK_DGRAM is a datagram-based protocol, that involves NO connection. You send any number of datagrams and receive any number of datagrams. It's an "unreliable service" in the sense that the data that is read by the receiver can be out-of-order from the sender’s writes; In file `config.ini` setup under `CLIENTUDP` the host to where you want to send data (your laptop for instance) and a PORT that is not being used. Then you can run in your laptop:

```sh
$ nc -ulk <PORT>
```

That will act as a server listining on PORT.

#### Mode: TCP

`python imu.py tcp` : TCP/SOCK_STREAM is a connection-based protocol. It is a "reliable" or "confirmed" service, in that packets are delivered, in order, or the connection terminates. The guarantee is that you get notified if the data might not have been delivered. In file `config.ini` setup under `SERVERTCP` select a PORT and you can run in the RPi a client in as the one below written in Python:

    import socket

    HOST = 'localhost'
    PORT = 5006

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        print(repr(data))

    s.close()

#### Mode: LOG

`python imu.py log` : This uses a logging approach by appending every read to `sensor.log` file. In this case you can open the file and analyze the data. As a communication process, given that the data is being appended to the end of the log file, you can opt by reading the end of the log file as a stream of data;

### Worth checking:

- https://blog.datasyndrome.com/a-tale-of-two-kafka-clients-c613efab49df - about python-kafka library failing to retrieve all messages

### Contributing

Review [the contributing guidelines](CONTRIBUTING.md) before you make your awesome contribution

### License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE)
