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
        
        self.ser.write("Hi from the mothership!".encode("utf-8"))

# Driver code
        
ser = SerialComms().with_baudrate(115200).with_port("/dev/cu.usbserial-141430").connect()