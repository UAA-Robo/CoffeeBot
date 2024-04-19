"""
To test, plug in the arduino (that's running ArduinoCode/ArduinoPiSerial/ArduinoPiSerial.ino),
replace the .with_port("...") with the proper port, and run python3 SerialComms.py
"""

import threading
import time
import math

from Simulation.main import Simulation
from Brain.Controller import Controller
from Brain.SerialComms import SerialComms

PI = math.pi

# Read inputs
def read_serial_data(ser):
    while True:
        if ser.ser.in_waiting > 0:  # Check if data is available
            data = ser.read_line()
            if data:
                print("Read:", data)
        time.sleep(0.5)  # Small delay to prevent hogging the CPU



def main() -> None:

    # try:
    ser = SerialComms().with_baudrate(9600).with_port("COM7") # /dev/cu.usbserial-AH03B2I9 COM13
    ser.connect()
    # Create and start a new thread for reading serial data
    thread = threading.Thread(target=read_serial_data, args=[ser])
    # thread.start()
    # except:
    #     ser = None
    #     print("Arduino NOT connected!")
    #    # TODO better error catching
    
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
        if ser:
            print("---------------------------HERERERER", ser)
            ser.write_line(f"M1V{joint_1_control * STEPS_PER_SEC}\n")
            ser.write_line(f"M2V{joint_2_control * STEPS_PER_SEC}\n")
            ser.write_line(f"M3V{joint_3_control * STEPS_PER_SEC}\n")
            ser.write_line(f"M4V{joint_4_control * STEPS_PER_SEC}\n")
            ser.write_line(f"M5V{joint_5_control * STEPS_PER_SEC}\n")
            ser.write_line(f"M6V{joint_6_control * STEPS_PER_SEC}\n")

        time.sleep(0.1)  # 1/240



if __name__ == "__main__":
    main()