#include "Buzzer.h"

Buzzer buzzer;

void setup() {
  // put your setup code here, to run once:
  pinMode(8, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  buzzer.SoundPlay()
}
