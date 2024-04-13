#include <AccelStepper.h>

#define dir_pin_1 2
#define step_pin_1 3

#define dir_pin_2 4
#define step_pin_2 5

#define dir_pin_3 6
#define step_pin_3 7

#define dir_pin_4 8
#define step_pin_4 9

#define dir_pin_5 10
#define step_pin_5 11

#define dir_pin_6 12
#define step_pin_6 13

// Initialize AccelStepper for six motors
AccelStepper stepper_1(AccelStepper::DRIVER, step_pin_1, dir_pin_1);
AccelStepper stepper_2(AccelStepper::DRIVER, step_pin_2, dir_pin_2);
AccelStepper stepper_3(AccelStepper::DRIVER, step_pin_3, dir_pin_3);
AccelStepper stepper_4(AccelStepper::DRIVER, step_pin_4, dir_pin_4);
AccelStepper stepper_5(AccelStepper::DRIVER, step_pin_5, dir_pin_5);
AccelStepper stepper_6(AccelStepper::DRIVER, step_pin_6, dir_pin_6);

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 bps

    stepper_1.setMaxSpeed(400);
    stepper_1.setAcceleration(500);
    stepper_2.setMaxSpeed(400);
    stepper_2.setAcceleration(500);
    stepper_3.setMaxSpeed(400);
    stepper_3.setAcceleration(500);
    stepper_4.setMaxSpeed(400);
    stepper_4.setAcceleration(500);
    stepper_5.setMaxSpeed(400);
    stepper_5.setAcceleration(500);
    stepper_6.setMaxSpeed(400);
    stepper_6.setAcceleration(500);

}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read until newline character
    if (input.length() > 0) {
      int speed = input.toInt();  // Convert read string to integer
      Serial.println(speed);  // Echo the speed back for debugging
      if (speed == 0) {
        // Stop all steppers if speed is 0
        stepper_1.stop();
        stepper_2.stop();
        stepper_3.stop();
        stepper_4.stop();
        stepper_5.stop();
        stepper_6.stop();
      } else {
        // Set new speed and move
        stepper_1.setSpeed(speed); // Steps/per second
        stepper_2.setSpeed(speed);
        stepper_3.setSpeed(speed);
        stepper_4.setSpeed(speed);
        stepper_5.setSpeed(speed);
        stepper_6.setSpeed(speed);
      }
    }
  }


  // Continue moving steppers to new positions
  stepper_1.runSpeed();
  stepper_2.runSpeed();
  stepper_3.runSpeed();
  stepper_4.runSpeed();
  stepper_5.runSpeed();
  stepper_6.runSpeed();
}
