#include <Arduino.h>

const int button = 4;
int buttonVal = 0;

void setup()
{
  // initialize LED digital pin as an output.
  Serial.begin(9600);

  pinMode(button, INPUT);

}

void loop()
{
  buttonVal = digitalRead(button);
  if(buttonVal == 1){
      Serial.println("Test");
  }

  delay(500);
}
