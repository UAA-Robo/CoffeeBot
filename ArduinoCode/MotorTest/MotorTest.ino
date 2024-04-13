#include <AccelStepper.h>
#define dir_pin_5 10
#define step_pin_5 11

#define dir_pin_6 12  // Direction
#define step_pin_6 13  // PUL
 



#define steps_per_rev 200

// Initialize AccelStepper for two motors
AccelStepper stepper_6(AccelStepper::DRIVER, step_pin_6, dir_pin_6);
AccelStepper stepper_5(AccelStepper::DRIVER, step_pin_5, dir_pin_5);

void setup() {
  // Set the maximum speed and acceleration:
  stepper_6.setMaxSpeed(400);  // steps/second
  stepper_6.setAcceleration(500); // steps/second^2
  stepper_5.setMaxSpeed(400);
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

