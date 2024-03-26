from inputs import get_gamepad
import threading


class Controller:

    MAX_JOYSTICK_VALUE = pow(2, 15)
    MAX_TRIGGER_VALUE = pow(2, 8)

    def __init__(self) -> None:
        


        self._left_x = 0.0
        self._left_y = 0.0
        self._right_x = 0.0
        self._right_y = 0.0
        self._a_btn = 0
        self._b_btn = 0
        self._x_btn = 0
        self._y_btn = 0
        self._left_bmp = 0
        self._right_bmp = 0
        self._left_trigger = 0
        self._right_trigger = 0
        self._dpad_up = 0
        self._dpad_down = 0
        self._dpad_left = 0
        self._dpad_right = 0
        self._left_thumb = 0
        self._right_thumb = 0
        self._back_btn = 0
        self._start_btn = 0

        self._read_thread = threading.Thread(target=self._read_inputs, args=())
        self._read_thread.setDaemon(True)
        self._read_thread.start()
    
    def _read_inputs(self) -> None:
        while True:
            events = get_gamepad()
            for event in events:
                match event.code:
                    case "ABS_X": self._left_x = event.state / self.MAX_JOYSTICK_VALUE
                    case "ABS_Y": self._left_y = event.state / self.MAX_JOYSTICK_VALUE
                    case "ABS_RX": self._right_x = event.state / self.MAX_JOYSTICK_VALUE
                    case "ABS_RY": self._right_y = event.state / self.MAX_JOYSTICK_VALUE
                    case "BTN_SOUTH": self._a_btn = event.state
                    case "BTN_EAST": self._b_btn = event.state
                    case "BTN_WEST": self._x_btn = event.state
                    case "BTN_NORTH": self._y_btn = event.state
                    case "BTN_TL": self._left_bmp = event.state
                    case "BTN_TR": self._right_bmp = event.state
                    case "ABS_Z": self._left_trigger = event.state / self.MAX_TRIGGER_VALUE
                    case "ABS_RZ": self._right_trigger = event.state / self.MAX_TRIGGER_VALUE
                    case "BTN_TRIGGER_HAPPY3": self._dpad_up = event.state
                    case "BTN_TRIGGER_HAPPY4": self._dpad_down = event.state
                    case "BTN_TRIGGER_HAPPY1": self._dpad_left = event.state
                    case "BTN_TRIGGER_HAPPT2": self._dpad_right = event.state
                    case "BTN_THUMBL": self._left_thumb = event.state
                    case "BTN_THUMBR": self._right_thumb = event.state
                    case "BTN_START": self._back_btn = event.state
                    case "BTN_SELECT": self._start_btn = event.state

    def print_all_inputs(self) -> None:
        print(f"Left Joystick: ({self._left_x}, {self._left_y})")
        print(f"Right Joystick: ({self._right_x}, {self._right_y})")
        print(f"Left Trigger: {self._left_trigger}")
        print(f"Right Trigger: {self._right_trigger}")
        print(f"Left Bumper: {self._left_bmp}")
        print(f"Right Bumper: {self._right_bmp}")
        print(f"Button A: {self._a_btn}")
        print(f"Button B: {self._b_btn}")
        print(f"Button X: {self._x_btn}")
        print(f"Button Y: {self._y_btn}")
        print(f"D-pad Up: {self._dpad_up}")
        print(f"D-pad Down: {self._dpad_down}")
        print(f"D-pad Left: {self._dpad_left}")
        print(f"D-pad Right: {self._dpad_right}")
        print(f"Back Button: {self._back_btn}")
        print(f"Start Button: {self._start_btn}")