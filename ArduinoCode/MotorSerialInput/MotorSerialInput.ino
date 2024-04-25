#include <AccelStepper.h>
#include <Servo.h>



Servo claw_servo;

int claw_position;

const int STEPPER_COUNT = 6;

void setup() {

  claw_servo.attach(A0);
  claw_position = claw_servo.read();

}

void loop() {
  claw_servo.write(180);
  delay(3000);
  claw_servo.write(0);
  delay(3000);
}
