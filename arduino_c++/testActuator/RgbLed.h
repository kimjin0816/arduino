#pragma once

#define DEF_PORT_R	(5)
#define DEF_PORT_G	(6)
#define DEF_PORT_B	(7)

#define CHECK_R (1)
#define CHECK_G (2)
#define CHECK_B (4)

#define DELAY_LED (1000)

//CT_YELLOW == 3 =  1+2
//CT_PINK  == 5 = 1+4
//CT_CYAN == 6 = 2+4
enum ColorType
{
	CT_BLACK = 0, CT_RED, CT_GREEN, CT_YELLOW, CT_BLUE, CT_PINK
};

class RgbLed
{
public:
	RgbLed(void) { setPort(DEF_PORT_R, DEF_PORT_G, DEF_PORT_B); } // 생성자
	~RgbLed() {}	// 소멸자, 파괴자

	void setPort(int nPortR, int nPortG, int nPortB)
	{
		m_nPortR = nPortR, m_nPortG = nPortG, m_nPortB = nPortB;
	}

	void setup(void) { initLed(); }

	//7가지의 색을 출력하기 위한 함수
	void displayLed() {
		for (int i = 1; i <= 7; i++) {
			turnRgbLed(i);
			delay(DELAY_LED);
		}
	}

	void turnRed(bool bOn)
	{
		if (bOn) digitalWrite(m_nPortR, HIGH);
		else digitalWrite(m_nPortR, LOW);
	}

	void turnGreen(bool bOn)
	{
		if (bOn) digitalWrite(m_nPortG, HIGH);
		else digitalWrite(m_nPortG, LOW);
	}

	void turnBlue(bool bOn)
	{
		if (bOn) digitalWrite(m_nPortB, HIGH);
		else digitalWrite(m_nPortB, LOW);
	}

private:
	int m_nPortR, m_nPortG, m_nPortB; // RGB 포트

	void initLed(void)
	{
		pinMode(m_nPortR, OUTPUT);
		pinMode(m_nPortG, OUTPUT);
		pinMode(m_nPortB, OUTPUT);
	}

	// RGB 7가지 색
	void turnRgbLed(int nColor) {
		int nR = nColor & CHECK_R;  // &: 비트 단위 and 연산
		int nG = nColor & CHECK_G;
		int nB = nColor & CHECK_B;
		digitalWrite(DEF_PORT_R, (nR) ? HIGH : LOW);
		digitalWrite(DEF_PORT_G, (nG) ? HIGH : LOW);
		digitalWrite(DEF_PORT_B, (nB) ? HIGH : LOW);
	}
};