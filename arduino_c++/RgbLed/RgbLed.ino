#include "RgbLed.h"

RgbLed rgbLed;

void setup() {
  // put your setup code here, to run once:
  rgbLed.setup();
}

void loop() {
  // put your main code here, to run repeatedly:
  rgbLed.turnRed(true);
  rgbLed.turnGreen(false);
  rgbLed.turnBlue(false);
  delay(1000);

  rgbLed.turnRed(false);
  rgbLed.turnGreen(true);
  rgbLed.turnBlue(false);
  delay(1000);

  rgbLed.turnRed(false);
  rgbLed.turnGreen(false);
  rgbLed.turnBlue(true);
  delay(1000);
}
