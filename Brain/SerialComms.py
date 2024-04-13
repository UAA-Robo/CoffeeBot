"""
This prints out any data recieved from the arduino connected via the USB
To test, plug in the arduino (that's running ArduinoCode/ArduinoPiSerial/ArduinoPiSerial.ino),
replace the .with_port("..."), and run python3 SerialComms.py
"""
import serial as serial

class SerialComms:
    def __init__(self) -> None:
        self.baudrate: int = None
        self.port: str = None
        self.ser: serial.Serial = None

    def with_baudrate(self, baud: int) -> 'SerialComms':
        self.baudrate = baud
        return self
    
    def with_port(self, port: str) -> 'SerialComms':
        self.port = port
        return self
    
    def connect(self) -> bool:
        if self.baudrate is None or self.port is None: raise IOError
        self.ser = serial.Serial(
            self.port,
            self.baudrate,
            8,
            "N",
        )
        try:
            self.ser.open()
        except serial.SerialException as e:
            print(e)
        
        #self.ser.write_line("Hi from the mothership!")

    def read_line(self):
        return self.ser.readline().decode("utf-8")
    
    def write_line(self, message:str) -> None:
        self.ser.write(message.encode("utf-8"))

