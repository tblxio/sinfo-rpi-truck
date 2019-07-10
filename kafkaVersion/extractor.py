import configparser
import socket
import logging
from logging.handlers import RotatingFileHandler
import time
import threading
from kafka import KafkaProducer


def loop_udp(imu, poll_interval, fields):
    """LOOP TO SEND DATA - UDP/SOCK_DGRAM
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = str(config['CLIENTUDP']['HOST'])
    port = int(config['CLIENTUDP']['PORT'])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    printCounter = 0
    while True:

        if imu.IMURead():
            data = imu.getIMUData()
            selected_data = [data.get(key) for key in fields]
            sock.sendto(str(selected_data), (host, port))

            if printCounter % 100 == 0:
                print selected_data

            time.sleep(poll_interval*1.0/1000.0)
            printCounter += 1


def loop_tcp(imu, poll_interval):
    """LOOP TO SEND DATA SERVER- TCP/SOCK_STREAM
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = str(config['SERVERTCP']['HOST'])
    port = int(config['SERVERTCP']['PORT'])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    printCounter = 0
    while True:
        print 'waiting connection'
        conn, addr = s.accept()

        print 'Client connection accepted ', addr
        while True:
            if imu.IMURead():
                try:
                    data = imu.getIMUData()
                    selected_data = [data.get(key) for key in fields]
                    conn.send(str(selected_data))

                    if printCounter % 100 == 0:
                        print selected_data

                    time.sleep(poll_interval*1.0/1000.0)
                    printCounter += 1
                except socket.error, msg:
                    print 'Client connection closed', addr
                    break
    conn.close()


def loop_log(imu, poll_interval, fields):
    """LOOP TO LOG DATA - Rolling log file
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = str(config['LOG']['FILENAME'])
    maxBytes = int(config['LOG']['MAXBYTES'])
    backupCount = int(config['LOG']['BACKUPCOUNT'])

    # logging setup
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = RotatingFileHandler(filename=filename,
                                  maxBytes=maxBytes,
                                  backupCount=backupCount)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    printCounter = 0
    while True:
      if imu.IMURead():
        data = imu.getIMUData()
        selected_data = [data.get(key) for key in fields]
        logger.info(selected_data)

        if printCounter % 100 == 0:
            print selected_data

        time.sleep(poll_interval*1.0/1000.0)
        printCounter += 1


def loop_producer(imu, poll_interval, fields):
    """LOOP KAFKA PRODUCER
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config['PRODUCER']

    class Producer(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.stop_event = threading.Event()

        def stop(self):
            self.stop_event.set()

        def run(self):
            producer = KafkaProducer(bootstrap_servers=config['KAFKA_BROKER'],
                                     sasl_plain_username=config['KAFKA_USERNAME'],
                                     sasl_plain_password=config['KAFKA_PASSWORD'],
                                     security_protocol='SASL_SSL',
                                     sasl_mechanism='PLAIN',
                                     ssl_check_hostname=False,
                                     retries=5,
                                     ssl_cafile=config["SSL_CAFILE"],
                                     ssl_certfile=config["SSL_CERTFILE"],
                                     ssl_keyfile=config["SSL_KEYFILE"])

            printCounter = 0
            while not self.stop_event.is_set():
              if imu.IMURead():
                data = imu.getIMUData()
                selected_data = str([data.get(key) for key in fields])
                producer.send(config["TOPIC"], str.encode(selected_data))

                if printCounter % 100 == 0:
                    print selected_data

                time.sleep(poll_interval*1.0/1000.0)
                printCounter += 1

    producer = Producer()
    producer.daemon = True
    producer.start()
    
    while True:
        time.sleep(1)

