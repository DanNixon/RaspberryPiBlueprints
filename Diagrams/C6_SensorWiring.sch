EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:arduino_shieldsNCL
LIBS:connector
LIBS:dev_boards
LIBS:general_ic
LIBS:misc_components
LIBS:modules
LIBS:v_regs
LIBS:C6_ArduinoWiring-cache
EELAYER 24 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Label 1500 1800 2    60   ~ 0
WIND_DIR_A
Text Label 1900 1800 0    60   ~ 0
ARDUINO_A0
Wire Wire Line
	1500 1800 1900 1800
Wire Wire Line
	1700 1900 1700 1800
Connection ~ 1700 1800
Text Label 1500 1600 2    60   ~ 0
WIND_DIR_B
Text Label 1900 2500 0    60   ~ 0
ARDUINO_GND
Text Label 1900 1600 0    60   ~ 0
ARDUINO_5V
Wire Wire Line
	1500 1600 1900 1600
Wire Wire Line
	1700 2400 1700 2500
Wire Wire Line
	1700 2500 1900 2500
$Comp
L R R3
U 1 1 5473B503
P 3200 2150
F 0 "R3" V 3280 2150 40  0000 C CNN
F 1 "R" V 3207 2151 40  0000 C CNN
F 2 "" V 3130 2150 30  0000 C CNN
F 3 "" H 3200 2150 30  0000 C CNN
	1    3200 2150
	1    0    0    -1  
$EndComp
$Comp
L LDR R2
U 1 1 5473B548
P 3200 1450
F 0 "R2" V 3280 1450 50  0000 C CNN
F 1 "LDR" V 3200 1450 50  0000 C CNN
F 2 "" H 3200 1450 60  0000 C CNN
F 3 "" H 3200 1450 60  0000 C CNN
	1    3200 1450
	1    0    0    -1  
$EndComp
Text Label 3400 2500 0    60   ~ 0
ARDUINO_GND
Text Label 3400 1100 0    60   ~ 0
ARDUINO_5V
Wire Wire Line
	3400 1100 3200 1100
Wire Wire Line
	3200 1100 3200 1200
Wire Wire Line
	3200 1700 3200 1900
Wire Wire Line
	3200 2400 3200 2500
Wire Wire Line
	3200 2500 3400 2500
Text Label 3400 1800 0    60   ~ 0
ARDUINO_A1
Wire Wire Line
	3400 1800 3200 1800
Connection ~ 3200 1800
$Comp
L R R1
U 1 1 5473B458
P 1700 2150
F 0 "R1" V 1780 2150 40  0000 C CNN
F 1 "R" V 1707 2151 40  0000 C CNN
F 2 "" V 1630 2150 30  0000 C CNN
F 3 "" H 1700 2150 30  0000 C CNN
	1    1700 2150
	1    0    0    -1  
$EndComp
$EndSCHEMATC
