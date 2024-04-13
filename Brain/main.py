"""
This sends signals to the Arduino (ArduinoCode/ArduinoSerialInput/ArduinoSerialInput.ino) to 
control 6 stepper motors. Python 3.10 or later required
"""
from SerialComms import SerialComms
import threading
import time
from Controller import Controller

# Driver code
        
ser = SerialComms().with_baudrate(9600).with_port("COM7") # /dev/cu.usbserial-AH03B2I9
ser.connect()

controller = Controller()

# Read inputs
def read_serial_data():
    while True:
        if ser.ser.in_waiting > 0:  # Check if data is available
            data = ser.read_line()
            if data:
                print("Read:", data)
        time.sleep(0.5)  # Small delay to prevent hogging the CPU

# Create and start a new thread for reading serial data
thread = threading.Thread(target=read_serial_data)
thread.start()

# Send Speed to Motor
while True:
    input = abs(controller._left_y) # TODO FIX PRIVATE ACCESS, allow negatives
    speed = input * 400  # Scale from 0 to 200
    #print("Speed: ", speed)
    ser.write_line(str(speed) + '\n')
    time.sleep(0.1)
