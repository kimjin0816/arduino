/* [Actuator(구동기) 구현]
1. 모터: servo motor, DC motor
 - 0도 -> 180도 -> 0도
2. 3색 LED
 - 7개 색깔을 1초씩 출력
3. 부저(buzzer)
 - 도레미파솔라시도를 1초씩 생성
4. 모든 actuator를 클래스로 구현되어야 함
*/

//#include "DcMotor.h"
#include "RgbLed.h"
#include "MyServo.h"
#include "Buzzer.h"

//DcMotor dcMotor;
RgbLed rgbLed;
MyServo myServo;
Buzzer buzzer;

void setup() {
  // put your setup code here, to run once:
  rgbLed.setup();
  myServo.setup();
  buzzer.setup();
}

void loop() {
  // put your main code here, to run repeatedly:
  myServo.move(0);
  myServo.move(180);
  rgbLed.displayLed();
  buzzer.play(NT_DO, 1000);
  buzzer.play(NT_RE, 1000);
  buzzer.play(NT_MI, 1000);
  buzzer.play(NT_FA, 1000);
  buzzer.play(NT_SOL, 1000);
  buzzer.play(NT_LA, 1000);
  buzzer.play(NT_SI, 1000);
  buzzer.play(NT_DDO, 1000);
}