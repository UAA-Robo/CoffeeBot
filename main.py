import threading
import time
import math

from Simulation.main import Simulation
from Brain.Controller import Controller
from Brain.SerialComms import SerialComms

PI = math.pi

def main() -> None:
    ser = SerialComms().with_baudrate(9600).with_port("COM13") # /dev/cu.usbserial-AH03B2I9
    ser.connect()
    
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

        joint_1_control = Controller.adjust_for_deadzone(controller.left_joystick_X()) # J1 Swivel base
        joint_2_control = Controller.adjust_for_deadzone(controller.left_joystick_Y()) # J2 Main arm up/down
        
        if controller.right_bumper():
            joint_5_control = Controller.adjust_for_deadzone(controller.right_joystick_Y()) # J5 Wrist up/down
            joint_6_control = Controller.adjust_for_deadzone(controller.right_joystick_X()) # J6 Wrist swivel
            
        else:
            joint_3_control = Controller.adjust_for_deadzone(controller.right_joystick_Y()) # J3 Upper arm up/down
            joint_4_control = Controller.adjust_for_deadzone(controller.right_joystick_X()) # J4 Upper arm swivel
            
        

        # controller.print_all_inputs()
        simu.set_joint_speed(1, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_1_control)
        simu.set_joint_speed(2, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_2_control)
        simu.set_joint_speed(3, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * -joint_3_control)
        simu.set_joint_speed(4, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_4_control)
        simu.set_joint_speed(5, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * -joint_5_control)
        simu.set_joint_speed(6, STEPS_PER_SEC * REVOLUTIONS_PER_STEP * RADIANS_PER_REVOLUTION * joint_6_control)

        print(joint_1_control * STEPS_PER_SEC)

        # Send to arduino
        ser.write_line(f"M1V{joint_1_control * STEPS_PER_SEC}\n")
        ser.write_line(f"M2V{joint_2_control * STEPS_PER_SEC}\n")
        ser.write_line(f"M3V{joint_3_control * STEPS_PER_SEC}\n")
        ser.write_line(f"M4V{joint_4_control * STEPS_PER_SEC}\n")
        ser.write_line(f"M5V{joint_5_control * STEPS_PER_SEC}\n")
        ser.write_line(f"M6V{joint_6_control * STEPS_PER_SEC}\n")

        time.sleep(0.1)  # 1/240



if __name__ == "__main__":
    main()