Maplin Weather Instrument Driver
================================

An Arduino based driver for the Maplin rain sensor, wind direction and speed sensors and an LDR.

Serial Output
-------------

- Rain: ```RAIN_DETECT;```
- Wind speed: ```WIND_SPEED:RPM:n;```
- Wind direction: ```WIND_DIRECTION:ARB:n;```

Wiring
------

- Rain sensor between GND and digital pin 2
- Wind speed sensor (red and yellow) between GND and digital pin 3
- Wind direction sensor (black and green) between +5V and A0 with 10K pull down
- LDR between +5V and A1 with 4.7K pull down

Maplin links
------------

- [Rain sensor](http://www.maplin.co.uk/p/maplin-replacement-rain-gauge-for-n25frn96fyn96gy-n77nf)
- [Wind speed sensor](http://www.maplin.co.uk/p/maplin-replacement-wind-speed-sensor-for-n96fy-n82nf)
- [Wind direction sensor](http://www.maplin.co.uk/p/maplin-replacement-wind-direction-sensor-for-n96fyn96gy-n81nf)
