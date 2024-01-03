void setup() {
  // put your setup code here, to run once:
  // DC motor: port 2개 필요
  // motor 초기화
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(2, HIGH); // 5V 인가
digitalWrite(3, LOW);  // 0V 인가
delay(1000);
//역방향 회전
digitalWrite(2, LOW);
digitalWrite(3, HIGH);
delay(1000);
}
