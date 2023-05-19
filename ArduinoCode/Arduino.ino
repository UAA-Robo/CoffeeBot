

#include <Servo.h>

Servo arm6; //bottom arm servo
Servo arm9; //middle arm servo: 
Servo arm10; //arm servo closest to claw:
Servo claw11; 


void setup() {
  //Correspond servos with pins
  arm6.attach(6);
  arm9.attach(9);
  arm10.attach(10);
  claw11.attach(11);
  
}
 
void loop() {
  moveBot(0, 45, 60, 60); //init position
  delay(1000);
  moveBot(0, 45, 60, 35); //close claw
  delay(1000);

  moveBot(-60, 45, 60, 35);
  delay(100);

  moveBot(-60, 75, 60, 35);
  delay(100);

  moveBot(-40, 75, 60, 35);
  delay(100);

  moveBot(60, 75, 60, 35);
  delay(100);


  moveBot(60, 45, 60, 35);
  delay(100);

  moveBot(60, 45, 60, 35);

  delay(1000);

}


//Movement Functions

//moveArms6 is relative degrees, negative degrees is counterclockwise looking from thhe back of the motor itt its front
void moveArm6(int arm6Degrees) {
  int power = 20;

  //Increase power when going up because there is more load to lift (temporary solution)
  if (arm6Degrees < 0) { 
    power *= 1.85; 
  }
  rotateMotorDegrees(arm6, arm6Degrees, power);
}


//moveArm9 is absolute degree position
void moveArm9(int arm9Position) {
  //0 degrees is fully up, 180 degrees is down
  arm9Position = constrain(arm9Position, 0, 180);
  moveServoToPosition(arm9, arm9Position, 100);
}

//moveArm10 is absolute degree position
void moveArm10(int arm10Position) {
  // 0 degrees is rotated to the right, 180 degrees is rotated to the left (almost upside down)
  arm10Position = constrain(arm10Position, 0, 180);
  moveServoToPosition(arm10, arm10Position, 100);
}

//moveClaw11 is absolute degree position
void moveClaw11(int claw11Position) {
  //10 degrees is fully close, 100 is fully open (DO NOT MOVE CLAW all the way to 180 because it can't turn that way)
  claw11Position = constrain(claw11Position, 0, 100);
  moveServoToPosition(claw11, claw11Position, 100);
}

void moveBot (int arm6Position, int arm9Position, int arm10Position, int claw11Position) {
  moveArm6(arm6Position);
  moveArm9(arm9Position);
  moveArm10(arm10Position);
  moveClaw11(claw11Position);
  delay(15);
}

void rotateMotorDegrees(Servo motor, int degrees, int powerPercent) {
  if (degrees < 0) {
    degrees = - degrees;
    powerPercent = - powerPercent;
  }
  const double MAX_RPM = 30;
  //const double ERROR_COMPENSATION = 100; //subtracted from msecToWait so we don't overshoot (temporary jank solution)
  double rpm = fabs(MAX_RPM * powerPercent / 100.0);
  double msecToWait = degrees / 360.0 * 60000 / rpm;

  setMotorPower(motor, powerPercent);
  delay(msecToWait);
  setMotorPower(motor, 0);
}

 void setMotorPower(Servo motor, int powerPercent){
  powerPercent = constrain(powerPercent, -100, 100);

  const int SIGNAL_MIN = 1050;
  const int SIGNAL_MAX = 1950;
  int signalOutput = map(powerPercent, -100, 100, SIGNAL_MIN, SIGNAL_MAX); //map(value, fromLow, fromHigh, toLow, toHigh)
  motor.writeMicroseconds(signalOutput);
  
}

void moveServoToPosition(Servo servo, int position, int powerPercent) {
  int currPosition = servo.read();
  const double RPM = 66.67;
  double msecToWait  = 50;

  if (position > currPosition) {
    for (int i = currPosition; i <= position; ++i) {
      servo.write(i);
      delay(msecToWait);
    }
  }
  else {
    for (int i = currPosition; i >= position; --i) {
      servo.write(i);
      delay(msecToWait);
    }
  }

}





