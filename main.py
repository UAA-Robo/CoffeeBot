"""
To test, plug in the arduino (that's running ArduinoCode/ArduinoPiSerial/ArduinoPiSerial.ino),
replace the .with_port("...") with the proper port, and run python3 SerialComms.py
"""

import threading
import time

from Simulation.main import Simulation
from Brain.Controller import Controller
from Brain.SerialComms import SerialComms
from Motor import Motor, Servo

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

    motor_1 = Motor(1, simu, ser)
    motor_1.set_steps_per_rev(1600)
    motor_1.set_speed(256)
    motor_2 = Motor(2, simu, ser)
    motor_2.set_steps_per_rev(200)
    motor_2.set_speed(72)
    motor_3 = Motor(3, simu, ser)
    motor_3.set_speed(72)
    motor_4 = Motor(4, simu, ser)
    motor_4.set_speed(72)
    motor_5 = Motor(5, simu, ser)
    motor_5.set_speed(72)
    motor_6 = Motor(6, simu, ser)
    motor_6.set_speed(72)
    claw_servo = Servo(7, simu, ser)


    joint_1_control = 0.0
    joint_2_control = 0.0
    joint_3_control = 0.0
    joint_4_control = 0.0
    joint_5_control = 0.0
    joint_6_control = 0.0
    joint_7_control = 0

    while True:

        joint_1_control = Controller.adjust_for_deadzone(controller.left_joystick_X()) # J1 Swivel base
        joint_2_control = Controller.adjust_for_deadzone(controller.left_joystick_Y()) # J2 Main arm up/down
        if (abs(joint_1_control) > abs(joint_2_control)): joint_2_control = 0.0
        elif (abs(joint_2_control) > abs(joint_1_control)): joint_1_control = 0.0
        
        if controller.right_bumper():
            joint_5_control = Controller.adjust_for_deadzone(controller.right_joystick_Y()) # J5 Wrist up/down
            joint_6_control = Controller.adjust_for_deadzone(controller.right_joystick_X()) # J6 Wrist swivel
            if (abs(joint_5_control) > abs(joint_6_control)): joint_6_control = 0.0
            elif (abs(joint_6_control) > abs(joint_5_control)): joint_5_control = 0.0
            
        else:
            joint_3_control = Controller.adjust_for_deadzone(controller.right_joystick_Y()) # J3 Upper arm up/down
            joint_4_control = Controller.adjust_for_deadzone(controller.right_joystick_X()) # J4 Upper arm swivel
            if (abs(joint_3_control) > abs(joint_4_control)): joint_4_control = 0.0
            elif (abs(joint_4_control) > abs(joint_3_control)): joint_3_control = 0.0
        if controller.right_trigger(): joint_7_control = 1
        elif controller.left_trigger(): joint_7_control = -1
        else: joint_7_control = 0

        print(joint_3_control)
        motor_1.move(joint_1_control)
        motor_2.move(joint_2_control)
        motor_3.move(joint_3_control)
        motor_4.move(joint_4_control)
        motor_5.move(joint_5_control)
        motor_6.move(joint_6_control)
        claw_servo.move(joint_7_control)

        time.sleep(0.1)  # 1/240



if __name__ == "__main__":
    main()