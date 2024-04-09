#include <AccelStepper.h>


#define step_pin_6 5  // PUL
#define dir_pin_6 4  // Direction 

#define step_pin_5 7
#define dir_pin_5 6

#define steps_per_rev 200

// Initialize AccelStepper for two motors
AccelStepper stepper_6(AccelStepper::DRIVER, step_pin_6, dir_pin_6);
AccelStepper stepper_5(AccelStepper::DRIVER, step_pin_5, dir_pin_5);

void setup() {
  // Set the maximum speed and acceleration:
  stepper_6.setMaxSpeed(200);  // steps/second
  stepper_6.setAcceleration(500); // steps/second^2
  stepper_5.setMaxSpeed(200);
  stepper_5.setAcceleration(500);

  // Set the target positions
  stepper_6.moveTo(2 * steps_per_rev); // 2 Rev
  stepper_5.moveTo(3 * steps_per_rev); // 3 Rev
}

void loop() {
  // These functions continuously move the stepper motors to their target positions
  stepper_6.run();
  stepper_5.run();
}

