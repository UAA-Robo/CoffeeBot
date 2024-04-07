// void setup() {
//   pinMode(5, OUTPUT); // Set the PWM pin as an output
// }

// void loop() {
//   analogWrite(5, 128); // Generate a PWM signal with 50% duty cycle on pin 9
//   // No need to change the value in loop() if you want a constant PWM signal
// }

// const int stepPin = 4; // Step pin
// const int dirPin = 5;  // Direction pin

// void setup() {
//   pinMode(stepPin, OUTPUT);
//   pinMode(dirPin, OUTPUT);
// }

// void loop() {
//   digitalWrite(dirPin, HIGH); // Set the direction
//   digitalWrite(stepPin, HIGH); // Move one step
//   delay(1); // Wait
//   digitalWrite(stepPin, LOW); // Pull step pin low so the motor can prepare for the next step
//   delay(1); // Wait
//   // Add code to turn off or change direction as needed
// }

// https://youtu.be/p4334ADfdF4?si=Z9UwGLWrCInvMCsT
const int stepPin = 5;
const int dirPin = 6;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH); // Set the direction
}

void loop() {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(50); // You may need to adjust this delay
  digitalWrite(stepPin, LOW);
  delayMicroseconds(50);
}