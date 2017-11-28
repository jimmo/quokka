EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
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
LIBS:microbit-socket
LIBS:microbit
LIBS:microbit-adaptor-cache
EELAYER 25 0
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
$Comp
L microbit_edge J1
U 1 1 5A1D3513
P 2600 4100
F 0 "J1" H 2600 5450 50  0000 C CNN
F 1 "microbit_edge" H 2600 2750 50  0000 C CNN
F 2 "microbit:microbit_edge" H 2450 4100 50  0001 C CNN
F 3 "" H 2450 4100 50  0001 C CNN
	1    2600 4100
	-1   0    0    1   
$EndComp
$Comp
L microbit_smd_socket J2
U 1 1 5A1D43CC
P 5150 4100
F 0 "J2" H 5150 5450 50  0000 C CNN
F 1 "microbit_smd_socket" H 5150 2750 50  0000 C CNN
F 2 "microbit-socket:smd_socket" H 6650 4100 50  0001 C CNN
F 3 "" H 6650 4100 50  0001 C CNN
	1    5150 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 2900 3050 2900
Wire Wire Line
	3050 2900 3050 3100
Wire Wire Line
	3050 3100 2950 3100
Connection ~ 3050 3000
Wire Wire Line
	4550 5100 4450 5100
Wire Wire Line
	4450 5100 4450 5300
Wire Wire Line
	4450 5300 4550 5300
Wire Wire Line
	4350 5200 4550 5200
Connection ~ 4450 5200
Wire Wire Line
	4550 4800 4450 4800
Wire Wire Line
	4450 4800 4450 5000
Wire Wire Line
	4450 5000 4550 5000
Wire Wire Line
	4350 4900 4550 4900
Connection ~ 4450 4900
Wire Wire Line
	5750 2900 5850 2900
Wire Wire Line
	5850 2900 5850 3100
Wire Wire Line
	5850 3100 5750 3100
Wire Wire Line
	5750 3200 5850 3200
Wire Wire Line
	5850 3200 5850 3400
Wire Wire Line
	5850 3400 5750 3400
Connection ~ 5850 3300
Connection ~ 5850 3000
Text GLabel 3150 3000 2    60   Input ~ 0
MB_GND
Text GLabel 3150 3300 2    60   Input ~ 0
MB_3V3
Wire Wire Line
	2950 3200 3050 3200
Wire Wire Line
	3050 3200 3050 3400
Wire Wire Line
	3050 3400 2950 3400
Connection ~ 3050 3300
Text GLabel 3150 3500 2    60   Input ~ 0
MB_20
Text GLabel 3150 3600 2    60   Input ~ 0
MB_19
Text GLabel 3150 3700 2    60   Input ~ 0
MB_16
Text GLabel 3150 3800 2    60   Input ~ 0
MB_15
Text GLabel 3150 3900 2    60   Input ~ 0
MB_14
Text GLabel 3150 4000 2    60   Input ~ 0
MB_13
Text GLabel 3150 4100 2    60   Input ~ 0
MB_12
Text GLabel 3150 4200 2    60   Input ~ 0
MB_11
Text GLabel 3150 4300 2    60   Input ~ 0
MB_10
Text GLabel 3150 4400 2    60   Input ~ 0
MB_9
Text GLabel 3150 4500 2    60   Input ~ 0
MB_8
Text GLabel 3150 4600 2    60   Input ~ 0
MB_7
Text GLabel 3150 4700 2    60   Input ~ 0
MB_6
Text GLabel 3150 4800 2    60   Input ~ 0
MB_5
Text GLabel 3150 4900 2    60   Input ~ 0
MB_4
Text GLabel 3150 5000 2    60   Input ~ 0
MB_3
Text GLabel 3150 5100 2    60   Input ~ 0
MB_2
Text GLabel 3150 5200 2    60   Input ~ 0
MB_1
Text GLabel 3150 5300 2    60   Input ~ 0
MB_0
Wire Wire Line
	2950 3500 3150 3500
Wire Wire Line
	3150 3600 2950 3600
Wire Wire Line
	2950 3700 3150 3700
Wire Wire Line
	3150 3800 2950 3800
Wire Wire Line
	2950 3900 3150 3900
Wire Wire Line
	3150 4000 2950 4000
Wire Wire Line
	2950 4100 3150 4100
Wire Wire Line
	3150 4200 2950 4200
Wire Wire Line
	2950 4300 3150 4300
Wire Wire Line
	3150 4400 2950 4400
Wire Wire Line
	2950 4500 3150 4500
Wire Wire Line
	3150 4600 2950 4600
Wire Wire Line
	2950 4700 3150 4700
Wire Wire Line
	3150 4800 2950 4800
Wire Wire Line
	2950 4900 3150 4900
Wire Wire Line
	3150 5000 2950 5000
Wire Wire Line
	2950 5100 3150 5100
Wire Wire Line
	3150 5200 2950 5200
Wire Wire Line
	2950 5300 3150 5300
Text GLabel 5950 3000 2    60   Input ~ 0
MB_GND
Text GLabel 5950 3300 2    60   Input ~ 0
MB_3V3
Text GLabel 5950 3500 2    60   Input ~ 0
MB_20
Text GLabel 5950 3600 2    60   Input ~ 0
MB_19
Text GLabel 5950 3700 2    60   Input ~ 0
MB_16
Text GLabel 5950 3800 2    60   Input ~ 0
MB_15
Text GLabel 5950 3900 2    60   Input ~ 0
MB_14
Text GLabel 5950 4000 2    60   Input ~ 0
MB_13
Text GLabel 5950 4100 2    60   Input ~ 0
MB_12
Text GLabel 5950 4200 2    60   Input ~ 0
MB_11
Text GLabel 5950 4300 2    60   Input ~ 0
MB_10
Text GLabel 5950 4400 2    60   Input ~ 0
MB_9
Text GLabel 5950 4500 2    60   Input ~ 0
MB_8
Text GLabel 5950 4600 2    60   Input ~ 0
MB_7
Text GLabel 5950 4700 2    60   Input ~ 0
MB_6
Text GLabel 5950 4800 2    60   Input ~ 0
MB_5
Text GLabel 5950 4900 2    60   Input ~ 0
MB_4
Text GLabel 5950 5000 2    60   Input ~ 0
MB_3
Text GLabel 5950 5100 2    60   Input ~ 0
MB_2
Text GLabel 5950 5200 2    60   Input ~ 0
MB_1
Text GLabel 5950 5300 2    60   Input ~ 0
MB_0
Wire Wire Line
	5750 3500 5950 3500
Wire Wire Line
	5950 3600 5750 3600
Wire Wire Line
	5750 3700 5950 3700
Wire Wire Line
	5950 3800 5750 3800
Wire Wire Line
	5750 3900 5950 3900
Wire Wire Line
	5950 4000 5750 4000
Wire Wire Line
	5750 4100 5950 4100
Wire Wire Line
	5950 4200 5750 4200
Wire Wire Line
	5750 4300 5950 4300
Wire Wire Line
	5950 4400 5750 4400
Wire Wire Line
	5750 4500 5950 4500
Wire Wire Line
	5950 4600 5750 4600
Wire Wire Line
	5750 4700 5950 4700
Wire Wire Line
	5950 4800 5750 4800
Wire Wire Line
	5750 4900 5950 4900
Wire Wire Line
	5950 5000 5750 5000
Wire Wire Line
	5750 5100 5950 5100
Wire Wire Line
	5950 5200 5750 5200
Wire Wire Line
	5750 5300 5950 5300
Wire Wire Line
	2950 3000 3150 3000
Wire Wire Line
	2950 3300 3150 3300
Text GLabel 4350 5200 0    60   Input ~ 0
MB_GND
Text GLabel 4350 4900 0    60   Input ~ 0
MB_3V3
Text GLabel 4350 4700 0    60   Input ~ 0
MB_20
Text GLabel 4350 4600 0    60   Input ~ 0
MB_19
Text GLabel 4350 4500 0    60   Input ~ 0
MB_16
Text GLabel 4350 4400 0    60   Input ~ 0
MB_15
Text GLabel 4350 4300 0    60   Input ~ 0
MB_14
Text GLabel 4350 4200 0    60   Input ~ 0
MB_13
Text GLabel 4350 4100 0    60   Input ~ 0
MB_12
Text GLabel 4350 4000 0    60   Input ~ 0
MB_11
Text GLabel 4350 3900 0    60   Input ~ 0
MB_10
Text GLabel 4350 3800 0    60   Input ~ 0
MB_9
Text GLabel 4350 3700 0    60   Input ~ 0
MB_8
Text GLabel 4350 3600 0    60   Input ~ 0
MB_7
Text GLabel 4350 3500 0    60   Input ~ 0
MB_6
Text GLabel 4350 3400 0    60   Input ~ 0
MB_5
Text GLabel 4350 3300 0    60   Input ~ 0
MB_4
Text GLabel 4350 3200 0    60   Input ~ 0
MB_3
Text GLabel 4350 3100 0    60   Input ~ 0
MB_2
Text GLabel 4350 3000 0    60   Input ~ 0
MB_1
Text GLabel 4350 2900 0    60   Input ~ 0
MB_0
Wire Wire Line
	4550 4700 4350 4700
Wire Wire Line
	4350 4600 4550 4600
Wire Wire Line
	4550 4500 4350 4500
Wire Wire Line
	4350 4400 4550 4400
Wire Wire Line
	4550 4300 4350 4300
Wire Wire Line
	4350 4200 4550 4200
Wire Wire Line
	4550 4100 4350 4100
Wire Wire Line
	4350 4000 4550 4000
Wire Wire Line
	4550 3900 4350 3900
Wire Wire Line
	4350 3800 4550 3800
Wire Wire Line
	4550 3700 4350 3700
Wire Wire Line
	4350 3600 4550 3600
Wire Wire Line
	4550 3500 4350 3500
Wire Wire Line
	4350 3400 4550 3400
Wire Wire Line
	4550 3300 4350 3300
Wire Wire Line
	4350 3200 4550 3200
Wire Wire Line
	4550 3100 4350 3100
Wire Wire Line
	4350 3000 4550 3000
Wire Wire Line
	4550 2900 4350 2900
Wire Wire Line
	5750 3000 5950 3000
Wire Wire Line
	5750 3300 5950 3300
Text GLabel 7250 4900 0    60   Input ~ 0
MB_GND
Text GLabel 7250 4800 0    60   Input ~ 0
MB_3V3
Text GLabel 7250 4700 0    60   Input ~ 0
MB_20
Text GLabel 7250 4600 0    60   Input ~ 0
MB_19
Text GLabel 7250 4500 0    60   Input ~ 0
MB_16
Text GLabel 7250 4400 0    60   Input ~ 0
MB_15
Text GLabel 7250 4300 0    60   Input ~ 0
MB_14
Text GLabel 7250 4200 0    60   Input ~ 0
MB_13
Text GLabel 7250 4100 0    60   Input ~ 0
MB_12
Text GLabel 7250 4000 0    60   Input ~ 0
MB_11
Text GLabel 7250 3900 0    60   Input ~ 0
MB_10
Text GLabel 7250 3800 0    60   Input ~ 0
MB_9
Text GLabel 7250 3700 0    60   Input ~ 0
MB_8
Text GLabel 7250 3600 0    60   Input ~ 0
MB_7
Text GLabel 7250 3500 0    60   Input ~ 0
MB_6
Text GLabel 7250 3400 0    60   Input ~ 0
MB_5
Text GLabel 7250 3300 0    60   Input ~ 0
MB_4
Text GLabel 7250 3200 0    60   Input ~ 0
MB_3
Text GLabel 7250 3100 0    60   Input ~ 0
MB_2
Text GLabel 7250 3000 0    60   Input ~ 0
MB_1
Text GLabel 7250 2900 0    60   Input ~ 0
MB_0
Wire Wire Line
	7450 4700 7250 4700
Wire Wire Line
	7250 4600 7450 4600
Wire Wire Line
	7450 4500 7250 4500
Wire Wire Line
	7250 4400 7450 4400
Wire Wire Line
	7450 4300 7250 4300
Wire Wire Line
	7250 4200 7450 4200
Wire Wire Line
	7450 4100 7250 4100
Wire Wire Line
	7250 4000 7450 4000
Wire Wire Line
	7450 3900 7250 3900
Wire Wire Line
	7250 3800 7450 3800
Wire Wire Line
	7450 3700 7250 3700
Wire Wire Line
	7250 3600 7450 3600
Wire Wire Line
	7450 3500 7250 3500
Wire Wire Line
	7250 3400 7450 3400
Wire Wire Line
	7450 3300 7250 3300
Wire Wire Line
	7250 3200 7450 3200
Wire Wire Line
	7450 3100 7250 3100
Wire Wire Line
	7250 3000 7450 3000
Wire Wire Line
	7450 2900 7250 2900
$Comp
L Conn_01x21 J3
U 1 1 5A1D5E0A
P 7650 3900
F 0 "J3" H 7650 5000 50  0000 C CNN
F 1 "Conn_01x21" H 7650 2800 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x21_Pitch2.54mm" H 7650 3900 50  0001 C CNN
F 3 "" H 7650 3900 50  0001 C CNN
	1    7650 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 4800 7450 4800
Wire Wire Line
	7250 4900 7450 4900
$EndSCHEMATC
