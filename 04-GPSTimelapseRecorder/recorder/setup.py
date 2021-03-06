from setuptools import setup

setup(
    name='rpi-gps-timelapse',
    version='0.1.0',
    entry_points = {
        'console_scripts': ['gpstimelapse=gpstimelapse:run'],
    },
    description='A GPS enabled timelapse recorder script for the Raspberry Pi camera',
    classifiers=[
	'Natural Language :: English',
	'Programming Language :: Python :: 2.7',
    ],
    url='http://github.com/DanNixon/RaspberryPi-Blueprints',
    author='Dan Nixon',
    author_email='dan@dan-nixon.com',
    license='Apache',
    packages=['gpstimelapse'],
    include_package_data=True,
    zip_safe=False)
