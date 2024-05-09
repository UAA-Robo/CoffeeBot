import math

from Simulation.main import Simulation
from Brain.SerialComms import SerialComms


STEPS_PER_SEC = 50
DEFAULT_STEPS_PER_REV = 200
# REVOLUTIONS_PER_STEP = 1 / 200.0
RADIANS_PER_REVOLUTION = 2 * math.pi

class Motor:
    def __init__(self, id: int, simulation: Simulation, serial: SerialComms = None) -> None:
        self.ID = id
        self.current_velocity = 0.0
        self.previous_velocity = 0.0
        self.simulation = simulation
        self.serial = serial
        self.steps_per_rev = DEFAULT_STEPS_PER_REV
        self.speed = 1

    def set_steps_per_rev(self, value: int) -> None:
        self.steps_per_rev = value
    
    def set_speed(self, value: int) -> None:
        self.speed = value

    def _move_simulation(self) -> None:
        self.simulation.set_joint_speed(self.ID, self.current_velocity * (1 / float(self.steps_per_rev)) * RADIANS_PER_REVOLUTION / 48.0)

    def _move_serial(self) -> None:
        if self.serial:
            self.serial.write_line(f"M{self.ID}V{self.current_velocity}\n")

    def move(self, input: float) -> None:
        input = round(input, 1)
        self.current_velocity = STEPS_PER_SEC * input * self.speed
        self._move_simulation()
        if (abs(self.current_velocity - self.previous_velocity) >= 10.0): self._move_serial()

        self.previous_velocity = self.current_velocity

    def get_id(self) -> int: return self.ID

class Servo:
    def __init__(self, id: int, simulation: Simulation, serial: SerialComms = None) -> None:
        self.ID = id
        self.simulation = simulation
        self.serial = serial
        self.current_velocity = None
        self.previous_velocity = None
    
    def _move_simulation(self) -> None:
        # self.simulation.set_joint_speed(self.ID, self.current_velocity * 48)
        ...

    def _move_serial(self) -> None:
        if self.serial:
            self.serial.write_line(f"M{self.ID}V{self.current_velocity}\n")
            print("Moved motor ", self.ID)

    def move(self, input: float) -> None:
        self.current_velocity = input
        self._move_simulation()
        if self.current_velocity != self.previous_velocity: self._move_serial()

        self.previous_velocity = self.current_velocity

    def get_id(self) -> int: return self.ID