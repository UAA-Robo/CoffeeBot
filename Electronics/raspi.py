"""
Need a program that takes a list of instructions and sends the relavant commands to the arduino


"""


import pyserial

with serial.Serial('/dev/ttyS1', 19200, timeout=1) as ser:
    x = ser.read()          # read one byte
    s = ser.read(10)        # read up to ten bytes (timeout)
    line = ser.readline()   # read a '\n' terminated line


