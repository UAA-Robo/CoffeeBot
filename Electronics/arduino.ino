// C++ code
//
/*
  Sweep

  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013  by Scott Fitzgerald
  http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

int pos = 0;

Servo servo_3;
Servo servo_5;
Servo servo_9;
Servo servo_10;
Servo servo_11;


// Servos on pin 3,5,9,10,11

// Syntax of >servo var like servo_3<.attach(>pin number<, >min<, >max<)

void setup()
{
  // Set up servos 
  servo_3.attach(3, 500, 2500);
  servo_5.attach(5, 500, 2500);
  servo_9.attach(9, 500, 2500);
  servo_10.attach(10, 500, 2500);
  servo_11.attach(11, 500, 2500);
  
  // start serial for controll
  Serial.begin(9600);
}

void loop()
{
  
  Serial.println("Enter data:");
  while (Serial.available() == 0) {}     //wait for data available
  String teststr = Serial.readString();  //read until timeout
  teststr.trim();                        // remove any \r \n whitespace at the end of the String
  if (teststr == "red") {
    Serial.println("A primary color");
  } else {
    Serial.println("Something else");
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  // servos 1-5 input 
  
  // sweep the servo from 0 to 180 degrees in steps
  // of 1 degrees
  for (pos = 0; pos <= 180; pos += 1) {
    // tell servo to go to position in variable 'pos'
    servo_9.write(pos);
    // wait 15 ms for servo to reach the position
    delay(15); // Wait for 15 millisecond(s)
  }
  for (pos = 180; pos >= 0; pos -= 1) {
    // tell servo to go to position in variable 'pos'
    servo_9.write(pos);
    // wait 15 ms for servo to reach the position
    delay(15); // Wait for 15 millisecond(s)
  }
}