#pragma once

#include <Servo.h>

#define DEF_SERVO_PORT	(4)
//#define DEF_DC_MOTOR_PORT1	(2)
//#define DEF_DC_MOTOR_PORT2	(3)
#define SERVO_SPEED (360./1100.) // 단위: 각도/시간(msec)

class MyServo
{
public: // public member(외부 접근 가능)
	MyServo(void) { setPort(DEF_SERVO_PORT); } // 생성자(클래스가 생성될 때 호출되는 함수)
	~MyServo() {} // 파괴자(클래스가 파괴될 때 호출되는 함수)

	int getServoPos(void) const { return m_servo.read(); } // const 의미: 현재 프로퍼티를 변경시키지 않음(상수(constant)로 처리)
	void setPort(int nPort) { m_nPort = nPort; }
	void setup(void) { initMotor(); }

	void move(int nPos) // nPos: 0도 ~ 180도 범위로 입력
	{
		int nDiff = abs(nPos - getServoPos()); // 현재 모터 위치와 nPos와의 각도 차이
		int nDelay = int(nDiff / SERVO_SPEED + 0.5); // 결과: 모터 회전에 걸리는 시간(밀리초); 0.5 의미: 반올림
		m_servo.write(nPos);
		delay(nDelay);
	}

	//void move(int nPos) // nPos : 어떤 각도든지 이동; (+)이면 정방향 (-)이면 역방향
	//{
	//	int nDelay = int(abs(nPos) / SERVO_SPEED + 0.5);
	//	if (nPos >= 0) { setFwdMove(); }
	//	else { setBackMove(); }
	//	delay(nDelay);
	//	stopMotor();
	//}

private: // private member(외부 접근 불가능)
	int m_nPort; // m_: member란 뜻
	Servo m_servo; // Servo 클래스의 인스턴스를 m_servo로 선언

	void initMotor(void)
	{
		m_servo.attach(m_nPort);
	}

	//void setFwdMove(void) // forward move (정방향 이동)
	//{
	//	digitalWrite(m_nPort1, HIGH);
	//	digitalWrite(m_nPort2, LOW);
	//}

	//void setBackMove(void) // forward move (역방향 이동)
	//{
	//	digitalWrite(m_nPort1, LOW);
	//	digitalWrite(m_nPort2, HIGH);
	//}
};