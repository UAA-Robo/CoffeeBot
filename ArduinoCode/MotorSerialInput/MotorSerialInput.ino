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

AccelStepper steppers[6] = {
    AccelStepper(AccelStepper::DRIVER, step_pin_1, dir_pin_1),  // Stepper 1
    AccelStepper(AccelStepper::DRIVER, step_pin_2, dir_pin_2),  // Stepper 2
    AccelStepper(AccelStepper::DRIVER, step_pin_3, dir_pin_3),  // Stepper 3
    AccelStepper(AccelStepper::DRIVER, step_pin_4, dir_pin_4),  // Stepper 4
    AccelStepper(AccelStepper::DRIVER, step_pin_5, dir_pin_5),  // Stepper 5
    AccelStepper(AccelStepper::DRIVER, step_pin_6, dir_pin_6)   // Stepper 6
};

const int STEPPER_COUNT = 6;

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 bps

    for (int i=0; i < STEPPER_COUNT; i++) {
      steppers[i].setMaxSpeed(400);
      steppers[i].setAcceleration(500);
    }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read until newline character

    /* Takes inputs in form of:
          M1V100 = Motor 1, Velocity 100 steps/second
          M2V-100 = Motor 2, Velocity -200 steps/second (reverse direction) 
    */
    if (input.length() > 0) {
      char command_type = input[2];
      char device_type = input[0];
      if (command_type == 'V' && device_type == 'M') {
        int stepper_index = input.substring(1,2).toInt() - 1;
        int velocity = input.substring(3).toInt();
        Serial.println(velocity);  // Echo the speed back for debugging

        if (velocity == 0) steppers[stepper_index].stop();
        else steppers[stepper_index].setSpeed(velocity);

      }
    }
  }

  // Continue moving steppers to new positions
  for (int i=0; i < STEPPER_COUNT; i++) steppers[i].runSpeed();

}
