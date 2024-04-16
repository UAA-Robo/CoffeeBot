import threading
import time
import math

from Simulation.main import Simulation
from Brain.Controller import Controller

PI = math.pi

def main() -> None:
    
    controller = Controller()

    simu = Simulation()
    simu.setup()
    simulation_thread = threading.Thread(target=simu.start, args=())
    simulation_thread.start()

    # Setup ratios
    
    STEPS_PER_SEC = 50
    REVOLUTIONS_PER_STEP = 1 / 200.0
    RADIANS_PER_REVOLUTION = 2 * PI

    joint_1_control = 0.0
    joint_2_control = 0.0
    joint_3_control = 0.0
    joint_4_control = 0.0
    joint_5_control = 0.0
    joint_6_control = 0.0

    while True:

        joint_1_control = controller.left_joystick_X() # J1 Swivel base
        joint_2_control = controller.left_joystick_Y() # J2 Main arm up/down
        if controller.right_bumper():
            print("pressed!")
            joint_5_control = controller.right_joystick_Y() # J5 Wrist up/down
            joint_6_control = controller.right_joystick_X() # J6 Wrist swivel
        else:
            joint_3_control = controller.right_joystick_Y() # J3 Upper arm up/down
            joint_4_control = controller.right_joystick_X() # J4 Upper arm swivel
    
        # controller.print_all_inputs()
        simu.set_joint_speed(1, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_1_control)
        simu.set_joint_speed(2, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_2_control)
        simu.set_joint_speed(3, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * -joint_3_control)
        simu.set_joint_speed(4, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_4_control)
        simu.set_joint_speed(5, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * -joint_5_control)
        simu.set_joint_speed(6, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_6_control)

        time.sleep(1/240)



if __name__ == "__main__":
    main()