
// https://youtu.be/p4334ADfdF4?si=Z9UwGLWrCInvMCsT
const int stepPin = 5;
const int dirPin = 6;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  digitalWrite(dirPin, HIGH); // Set the direction

  // Turns 1 full rev when encoders set tto 200 pulses/rev
  // for (int i = 0; i< 200; i++) {
  //   digitalWrite(stepPin, HIGH);
  //   delayMicroseconds(50); // You may need to adjust this delay
  //   digitalWrite(stepPin, LOW);
  //   delayMicroseconds(1);

  // }
}

void loop() {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(100); // You may need to adjust this delay
    digitalWrite(stepPin, LOW);
    delayMicroseconds(100);
}