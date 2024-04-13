"""
This sends signals to the Arduino (ArduinoCode/ArduinoSerialInput/ArduinoSerialInput.ino) to 
control 6 stepper motors. Python 3.10 or later required
"""
from SerialComms import SerialComms
import threading
import time
from Controller import Controller

# Driver code
        
ser = SerialComms().with_baudrate(9600).with_port("/dev/cu.usbserial-AH03B2I9")
ser.connect()



def read_serial_data():
    while True:
        if ser.ser.in_waiting > 0:  # Check if data is available
            data = ser.read_line()
            if data:
                print("Read:", data)
        time.sleep(0.1)  # Small delay to prevent hogging the CPU

# Create and start a new thread for reading serial data
thread = threading.Thread(target=read_serial_data)
thread.start()

# Send Speed to Motor
for speed in range(50, 451, 50):
    #print("Speed: ", speed)
    ser.write_line(str(speed) + '\n')
    time.sleep(1)
