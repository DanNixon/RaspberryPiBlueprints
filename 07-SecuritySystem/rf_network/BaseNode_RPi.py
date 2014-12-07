#!/usr/bin/env python

import time, sys
from struct import *
from RF24 import *
from RF24Network import *
import paho.mqtt.client as mqtt

if len(sys.argv) < 3:
    print 'Usage BaseNode_RPi.py: [address] [port]'
    sys.exit(1)

RADIO = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
NETWORK = RF24Network(RADIO)

CHANNEL = 90
BASE_NODE_ADDR = 00

RADIO.begin()
time.sleep(0.1)
NETWORK.begin(CHANNEL, BASE_NODE_ADDR)

# Print some debug info
RADIO.printDetails()

def on_connect(client, userdata, flags, rc):
    global MQTT_CONNECTED
    MQTT_CONNECTED = rc == 0

MQTT_CLIENT = mqtt.Client()
MQTT_CLIENT.on_connect = on_connect
MQTT_CLIENT.connect(sys.argv[1], int(sys.argv[2]), 60)

while True:
    # Pump the network and MQTT client
    NETWORK.update()
    MQTT_CLIENT.loop()

    # Check for new messages
    while NETWORK.available():
        header, payload = NETWORK.read(15)
        payload_data = payload.split(',')

        topic = payload_data[0]
        message = payload_data[1].split(';')[0]

        MQTT_CLIENT.publish(topic, message)

    time.sleep(0.1)
