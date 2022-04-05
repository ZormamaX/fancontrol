# Import Modules
import serial
import time
import subprocess
import re
import json
import os
import sys

# Serial stuff
SerialObj = serial.Serial('/dev/ttyUSB0')

SerialObj.baudrate = 115200	# set Baud rate to 115200
SerialObj.bytesize = 8	# Number of data bits = 8
SerialObj.parity   ='N'	# No parity
SerialObj.stopbits = 1	# Number of Stop bits = 1

while True:

	time.sleep(3)	# Wait for serial, opening a port will take around 3 seconds

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
		FanSpeed_f = 255 * 0.2 # 20%
	elif temp > 45 and temp < 60:
		FanSpeed_f = 255 * 0.3 # 25%
	elif temp > 65 and temp < 70:
		FanSpeed_f = 255 * 0.5 # 50%
	elif temp > 70 and temp < 72:
		FanSpeed_f = 255 * 0.6 # 60%
	elif temp > 72 and temp < 75:
		FanSpeed_f = 255 * 0.75 # 75%
	elif temp > 75:
		FanSpeed_f = 255 * 0.85 # 85%

	FanSpeed = int(FanSpeed_f) 
	print(FanSpeed)

	# Send serial
	#BytesWritten = SerialObj.write()	# Write the 1st character in temp, which is enough to roughly determine temperature

	BytesWritten = SerialObj.write(FanSpeed.to_bytes(1, byteorder='big'))

	print('BytesWritten = ', BytesWritten)

	#SerialObj.close()	# Close the serial port
