#!/bin/bash

# To ensure that the OS is fully booted and SD access and CPU usage will be minimal
sleep 20

cd /home/pi
python player.py -d music --random -f 99.9 &
