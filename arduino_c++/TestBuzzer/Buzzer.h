//여기가 검사

#pragma once

#define DEF_BUZZER_PORT (8)

enum NoteType
{
	NT_DO = 523, NT_RE = 587, NT_MI = 659, NT_PA= 698, 
	NT_SOL = 783, NT_RA = 880, NT_SI = 987, NT_DDO = 1046
};

class Buzzer
{
public:
	Buzzer(void) { setPort(DEF_BUZZER_PORT); }  // 생성자
	~Buzzer(void) {} // 파괴자
	void setPort(int nPort)
	{
		m_nPort = nPort
	}

	void setup(void) { initBuzzer(); }

	void SoundPlay(int nNode, int nTime)
	{
		for (int i = 0; i <= 8; i++) 
		{
			tone(m_nPort, nNode, nTime);
			delay(1000);
		}
	}

private:
	int m_nPort;

	void initBuzzer(void)
	{
		pinMode(m_nPort, OUTPUT);
	}

};