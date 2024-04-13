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

#define dir_pin_6 12  // Direction
#define step_pin_6 13  // PUL
 

#define steps_per_rev 200

// Initialize AccelStepper for two motors
AccelStepper stepper_1(AccelStepper::DRIVER, step_pin_1, dir_pin_1);
AccelStepper stepper_2(AccelStepper::DRIVER, step_pin_2, dir_pin_2);
AccelStepper stepper_3(AccelStepper::DRIVER, step_pin_3, dir_pin_3);
AccelStepper stepper_4(AccelStepper::DRIVER, step_pin_4, dir_pin_4);
AccelStepper stepper_5(AccelStepper::DRIVER, step_pin_5, dir_pin_5);
AccelStepper stepper_6(AccelStepper::DRIVER, step_pin_6, dir_pin_6);


void setup() {
  // Set the maximum speed and acceleration:
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

  stepper_6.setMaxSpeed(400);  // steps/second
  stepper_6.setAcceleration(500); // steps/second^2


  // Set the target positions
  stepper_1.moveTo(3 * steps_per_rev); // 3 Rev
  stepper_2.moveTo(3 * steps_per_rev); // 3 Rev
  stepper_3.moveTo(3 * steps_per_rev); // 3 Rev
  stepper_4.moveTo(3 * steps_per_rev); // 3 Rev
  stepper_5.moveTo(3 * steps_per_rev); // 3 Rev
  stepper_6.moveTo(3 * steps_per_rev); // 2 Rev
  

}

void loop() {
  // These functions continuously move the stepper motors to their target positions
  stepper_1.run();
  stepper_2.run();
  stepper_3.run();
  stepper_4.run();
  stepper_5.run();
  stepper_6.run();

}

