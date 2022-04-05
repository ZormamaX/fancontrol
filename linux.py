# Import Modules
import serial
import time
import subprocess
import re
import json
import os
import sys
import serial.tools.list_ports

# Serial stuff
ports = list(serial.tools.list_ports.comports())
if ports:
	for p in ports:
		if "USB2.0-Serial" in p.description:
			port = p.device
			print("Arduino: ", port)
			if not "/dev/ttyUSB" in port:
				print("Arduino not found!")
else:
	print("Ports not found!")

try:
	SerialObj = serial.Serial(port)
	
	SerialObj.baudrate = 115200	# set Baud rate to 115200
	SerialObj.bytesize = 8	# Number of data bits = 8
	SerialObj.parity   ='N'	# No parity
	SerialObj.stopbits = 1	# Number of Stop bits = 1
except NameError:
	print("Arduino not found!")
	os.system("notify-send -u critical -t 30000 \"Arduino not connected!\" \"Please reconnect Arduino.\"")
	exit(0)

FanSpeed_f = 255 * 0.2 # 20%

#ports = list(serial.tools.list_ports.comports())
#if ports:
#	for p in ports:
#		if "USB2.0-Serial" in p.description:
#			port = p.device
#			print("Arduino: ", port)
#			if not "/dev/ttyUSB" in port:
#				print("Arduino not found!")
#else:
#	print("Ports not found!")
#
#try:
#	SerialObj = serial.Serial(port)
#	
#	SerialObj.baudrate = 115200	# set Baud rate to 115200
#	SerialObj.bytesize = 8	# Number of data bits = 8
#	SerialObj.parity   ='N'	# No parity
#	SerialObj.stopbits = 1	# Number of Stop bits = 1
#except NameError:
#	print("Arduino not found!")
#	os.system("notify-send -u critical -t 30000 \"Arduino not connected!\" \"Please reconnect Arduino.\"")
#	exit(0)


while True:
	# Read temps 
	cmd = os.popen('sensors -j')
	output = cmd.read()
	cmd.close()
	
	temp_json = json.loads(output)

	temp_float = temp_json['k10temp-pci-00c3']['Tdie']['temp1_input']
	temp = int(temp_float)
	print("CPU Temperature: ", temp)

	# Calculate fan speed
	if temp < 45:
		FanSpeed_target = 255 * 0.2 # 20%
	elif temp > 45 and temp < 65:
		FanSpeed_target = 255 * 0.2 # 30%
	elif temp > 65 and temp < 70:
		FanSpeed_target = 255 * 0.4 # 40%
	elif temp > 70 and temp < 72:
		FanSpeed_target = 255 * 0.4 # 40%
	elif temp > 72 and temp < 75:
		FanSpeed_target = 255 * 0.4 # 40%
	elif temp > 75:
		FanSpeed_target = 255 * 0.4 # 40%
	
	if FanSpeed_f < FanSpeed_target:
		FanSpeed_f = FanSpeed_f + 2
	elif FanSpeed_f > FanSpeed_target:
		FanSpeed_f = FanSpeed_f - 2
	
	FanSpeed = int(FanSpeed_f)
	print(FanSpeed)

	# Send serial
	#BytesWritten = SerialObj.write()	# Write the 1st character in temp, which is enough to roughly determine temperature
	try:
		BytesWritten = SerialObj.write(FanSpeed.to_bytes(1, byteorder='big'))
	except OSError:
		print("Arduino not found!")
		os.system("notify-send -u critical -t 30000 \"Arduino not connected!\" \"Please reconnect Arduino.\"")
		exit(0)

	print('BytesWritten = ', BytesWritten)

	#SerialObj.close()	# Close the serial port
	
	
	time.sleep(1)	# Wait and send a signal after 3 secs
