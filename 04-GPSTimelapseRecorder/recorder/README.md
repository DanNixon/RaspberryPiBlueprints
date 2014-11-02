GPS Timelapse Recorder
======================

A script to manage recording a timelapse with GPS metadata and
the option to limit the timelapse frame capture by distance moved
since the last capture.

Installation
------------

Requires the following libraries which must be installed manually:

- [python-picamera](http://picamera.readthedocs.org) which can be installed on the Pi using ```sudo apt-get install python-picamera```
- [pexif](https://github.com/bennoleslie/pexif) whcih (at the time of writing) must be installed by cloning the repo and running ```sudo python setup.py install``` (the version on installed by setuptools and pip will not work correctly with images from the Pi camera)

Once both are installed use ```sudo python setup.py install``` to install.

Usage
-----

Run ```gpstimelapse -h``` to get a description of all commands.

Example 1: ```gpstimelapse -i 5 -f captures -n frame_%d.jpg```
will capture a frame every 5 seconds with the folder
pattern ```./captures/0/frame_0.jpg```

Example 2: ```gpstimelapse -i 5 -f captures -n frame_%d.jpg -d 0.05```
will behave similar to example 1 but will only capture a new frame
if 50m have been traveled since the last capture.
