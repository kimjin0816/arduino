#pragma once

#include "StringTok.h"
#include "Voltmeter.h"
#include "LightSensor.h"
#include "MyServo.h"
#include "DcMotor.h"
#include "RgbLed.h"
#include "Buzzer.h"

class ArduinoHub
{
public:
	ArduinoHub(void) {}
	~ArduinoHub() {}

	void setup(void) // actuator �ʱ�ȭ
	{
		m_myServo.setup();
		m_dcMotor.setup();
		m_rgbLed.setup();
		m_buzzer.setup();
	}

	void start(void)
	{
		while (1) // 무한 반복
		{
			m_stInput.appendSerial();
			if (m_stInput.hasLine()) // 명령어 정상 입력
				exeCmd(); // 명령어 실행
		}
	}

	void exeCmd(void)
	{
    String sToken = m_stInput.cutToken().toString();
		if (sToken == "get" | sToken == "set") { exeGet(); }
		else { m_stInput.cutLine(); } // 잘못된 명령 -> 현재 줄을 삭제
	}

	void exeGet(void) // get 명령어 실행
	{
		// 1. 전압 읽기 : get volt
		String sToken = m_stInput.cutToken().toString();

		if (sToken == "volt") { exeVolt(); }
		else if (sToken == "light") { exeLight(); }
    else if (sToken == "lightstep") { exeLightStep(); }
		else if (sToken == "servo") { exeServo(); }
		else if (sToken == "led") { exeLed(); }
		else if (sToken == "buzzer") { exeBuzzer(); }
		else { m_stInput.cutLine(); }
	}

  

	void exeVolt()
	{
		double volt = m_voltmeter.getVolt();
		Serial.println(String(volt, 10)); // Serial에 출력
	}

	void exeLight() 
	{
		int nLightState = m_lightSensor.getLightState();
    Serial.println(m_lightSensor.lightStateToStr(nLightState));
	}

  void exeLightStep()
  {
    int nLightState = m_lightSensor.getLightState();
		Serial.println(String(nLightState));
  }

	void exeServo() 
	{
		String sToken = m_stInput.cutToken().toString();
		Serial.println("servo: " + sToken);
		m_myServo.move(sToken.toInt());
	}

	void exeLed()
	{
		String sToken = m_stInput.cutToken().toString();
		if (sToken == "red") { m_rgbLed.turnRed(true); }
		else if (sToken == "green") { m_rgbLed.turnGreen(true); }
		else if (sToken == "blue") { m_rgbLed.turnBlue(true); }
		else if (sToken == "yellow") { m_rgbLed.turnRed(true); m_rgbLed.turnGreen(true);}
		else if (sToken == "pink") { m_rgbLed.turnRed(true); m_rgbLed.turnBlue(true);}
		else if (sToken == "cyan") { m_rgbLed.turnBlue(true); m_rgbLed.turnGreen(true);}
		else if (sToken == "white") { m_rgbLed.turnRed(true); m_rgbLed.turnBlue(true); m_rgbLed.turnGreen(true); }
		else if (sToken == "none") { m_rgbLed.turnRed(false); m_rgbLed.turnBlue(false); m_rgbLed.turnGreen(false);}
		m_rgbLed.turnOffLED();
	}

	void exeBuzzer()
	{
		String sToken = m_stInput.cutToken().toString();
		String sToken1 = m_stInput.cutToken().toString();
		if (sToken == "DO") { m_buzzer.play(523, sToken1.toInt()); }
		else if (sToken == "RE") { m_buzzer.play(587, sToken1.toInt()); }
		else if (sToken == "MI") { m_buzzer.play(659, sToken1.toInt()); }
		else if (sToken == "FA") { m_buzzer.play(698, sToken1.toInt()); }
		else if (sToken == "SOL") { m_buzzer.play(783, sToken1.toInt()); }
		else if (sToken == "LA") { m_buzzer.play(880, sToken1.toInt()); }
		else if (sToken == "SI") { m_buzzer.play(987, sToken1.toInt()); }
	}

private:
	StringTok m_stInput;
	Voltmeter m_voltmeter;
	LightSensor m_lightSensor;
	MyServo m_myServo;
	DcMotor m_dcMotor;
	RgbLed m_rgbLed;
	Buzzer m_buzzer;
};