#include "DcMotor.h"

DCMotor dcMotor;

void setup() {
  // put your setup code here, to run once:
  dcMotor.setup();
}

void loop() {
  // put your main code here, to run repeatedly:
  dcMotor.move(180);   // 현재 각도 -> 180만큼 이동
  dcMotor.move(-180);  // 현재 각도(180도) -> -180만큼 이동
}