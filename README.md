# fancontrol
Fan controller made for prebuilt desktop PCs that don't allow controlling fans manually. Requires an Arduino (or similar microcontroller with PWM capabilities) to function.

Has some issues that I don't care too much to fix. One issue is the fans going at full speed on PC boot. This is because it takes a while for the Arduino to send the PWM signal to the fans to slow down them.

# Usage
1. You need an Arduino microcontroller (or similar with PWM capabilities)
2. Solder the PWM pin in the PC fans to the Arduino's pins 9, 10 or 11 (preferred configuration: fan in: pin 9, fan out: pin 10, CPU fan: pin 11. You can change the values in the Arduino code)
3. Connect the Arduino to a USB port of your preference and change the python code to have the corresponding port. I bodged a connector straight to the motherboard USB pins
4. Upload the code to your microcontroller and make the python script auto-start
5. If you're on Windows, change the file extension to .pyw so it doesn't open a terminal window
6. Make sure none of your electronics touch the PC case or components and don't cause a short circuit
