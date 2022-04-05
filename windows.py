# Import Modules
import serial
import time
import subprocess
import re
import json
import os
import sys
import serial.tools.list_ports
import wmi

# Set variables for later use
temp = 0
FanSpeed_f = 255 * 0.2 # 20%
FanSpeed_target = 255 * 0.2 # 20%

# Serial stuff

ports = list(serial.tools.list_ports.comports())
if ports:
	for p in ports:
		if "USB-SERIAL" in p.description:
			port = p.device
			#print("Arduino: ", port)
			if not "COM" in port:
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
	os.system("notifu /m \"Arduino not found!\" /p \"Please reconnect Arduino.\"")
	exit(0)

while True:
	ports = list(serial.tools.list_ports.comports())
	if ports:
		for p in ports:
			if "USB-SERIAL" in p.description:
				port = p.device
				print("Arduino: ", port)
				if not "COM" in port:
					print("Arduino not found!")
	else:
		print("Ports not found!")
	
	# Read temps WINDOWS
	w = wmi.WMI(namespace="root\OpenHardwareMonitor")
	temperature_infos = w.Sensor()
	
	for sensor in temperature_infos:
		if sensor.Name == "CPU Package" and sensor.SensorType == u'Temperature':
			temp = int(sensor.Value)
			print("CPU Temperature: ", temp)

	# Read temps LINUX
	#cmd = os.popen('sensors -j')
	#output = cmd.read()
	#cmd.close()
	
	#temp_json = json.loads(output)

	#temp_float = temp_json['k10temp-pci-00c3']['Tdie']['temp1_input']
	#temp = int(temp_float)
	#print("CPU Temperature: ", temp)

	# Calculate fan speed
	if temp < 45:
		FanSpeed_target = 255 * 0.2 # 20%
	elif temp > 45 and temp < 60:
		FanSpeed_target = 255 * 0.3 # 25%
	elif temp > 65 and temp < 70:
		FanSpeed_target = 255 * 0.45 # 45%
	elif temp > 70 and temp < 72:
		FanSpeed_target = 255 * 0.45 # 50%
	elif temp > 72 and temp < 75:
		FanSpeed_target = 255 * 0.45 # 45%
	elif temp > 75 and temp < 80:
		FanSpeed_target = 255 * 0.45 # 45%
	elif temp > 80:
		FanSpeed_target = 255 * 0.6 # 60%

	if FanSpeed_f < FanSpeed_target:
		FanSpeed_f = FanSpeed_f + 4
	elif FanSpeed_f > FanSpeed_target:
		FanSpeed_f = FanSpeed_f - 4

	FanSpeed = int(FanSpeed_f)
	print(FanSpeed)

	# Send serial
	#BytesWritten = SerialObj.write()	# Write the 1st character in temp, which is enough to roughly determine temperature
	try:
		BytesWritten = SerialObj.write(FanSpeed.to_bytes(1, byteorder='big'))
	except OSError:
		print("Arduino not found!")
		os.system("notifu /m \"Arduino not found!\" /p \"Please reconnect Arduino.\"")
		#exit(0)

	print('BytesWritten = ', BytesWritten)

	time.sleep(1)	# Wait 1 sec and start over

	#SerialObj.close()	# Close the serial port
