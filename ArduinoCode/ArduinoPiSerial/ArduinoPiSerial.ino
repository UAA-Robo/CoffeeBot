const unsigned long BAUDRATE = 57600;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(BAUDRATE);
}

int i = 0;

void loop()
{
  // put your main code here, to run repeatedly:
  i++;
  Serial.println(String(i)); // Send String via serial
  delay(2500);
}