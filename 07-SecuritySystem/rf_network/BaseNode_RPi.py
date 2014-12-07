#!/usr/bin/env python

import time
from struct import *
from RF24 import *
from RF24Network import *

radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
network = RF24Network(radio)

CHANNEL = 90
BASE_NODE_ADDR = 00

radio.begin()
time.sleep(0.1)
network.begin(CHANNEL, BASE_NODE_ADDR)

# Print some debug info
radio.printDetails()

while True:
    # Pump the network
    network.update()

    # Check for new messages
    while network.available():
        header, payload = network.read(15)
        print payload

    time.sleep(0.1)
