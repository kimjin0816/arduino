from serial import Serial
import time # time 모듈을 수입: 시간 관련 함수 집합체
import psycopg2
import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# public 멤버(클래스 외부에서 편하게 접근 가능): __이름__
# private 멤버(클래스 외부에서 접근 불가능(?, 특별한 부호 붙이면 접근 가능)): __이름
class PythonHub: # 클래스(객체의 설계도), 인스턴스(클래스로 만든 실체, 클래스로 만든 변수) 구별
    # Private 멤버: __로 시작하는 변수나 함수
    __defComName = 'COM3'
    __defComBps = 9600
    __defWaitTime = 0.5 # 단위: 초

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    

    # public 정적 멤버: 항상 위에 정의 -> 위에 정의되어야 밑에서 접근(호출 ) 가능
    def waitSerial(): # self가 없음 -> 클래스의 정적(static)멤버: 인스턴스 멤버에 접근하지 않음
        # PythonHub.__defWaitTime : 클래스 멤버에 접근할 때는 클래스명.(PythonHub.__defWaitTime)
        time.sleep(PythonHub.__defWaitTime) # 단위: 초  
    
    def wait(delaySec):
        time.sleep(delaySec)  
    
    # 생성자(constructor): 이름은 __init__로 고정
    def __init__(self, comName = __defComName, comBps = __defComBps): # comName: Serial 이름, comBps: Serial 속도
        #print('생성자 호출됨')
        # 멤버 변수 생성: 변수를 선언하지 않고 self.으로 변수를 추가; self는 클래스(PythonHub)로 만든 인스턴스에 접근하기 위한 키워드
        # Serial 클래스의 인스턴스 생성 -> self.ard에 할당
        self.ard = Serial(comName, comBps) # C++ 경우: Serial ard;
        self.clearSerial() # Serial 입력 버퍼 초기화
        self.clearVoltTuple() # 전압과 측정 시간을 위한 튜플 공간 확보
        self.conn = None # DB의 connection
        self.cur = None # DB의 cursor
        lights = ()
        lightSteps = ()
        lightTimes=()
        volts = ()
        voltTimes = ()
        
    # 소멸자(destructor): dlfmadms __del__으로 고정
    def __del__(self):
        print('소멸자 호출됨')
        if self.ard.isOpen(): # Serial이 열려(open)있는가?
            self.ard.close() # Serial을 닫음(close)   
            
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    # Serial 통신 메소드(멤버 함수)
    def writeSerial(self, sCmd):
        """
        Serial 포트에 데이터를 쓰는 메소드
    
        Parameters:
        - sCmd (str): 쓸 데이터로 문자열 형태여야 함
    
        Returns:
        - int: 쓰여진 바이트 수
        """
        btCmd = sCmd.encode()  # 문자열을 바이트로 인코딩
        nWrite = self.ard.write(btCmd)  # Serial 포트에 데이터 쓰기
        self.ard.flush()  # Serial 버퍼 비우기
        return nWrite

    def readSerial(self):
        """
        Serial 포트에서 데이터를 읽는 메소드
    
        Returns:
        - str: 읽은 데이터 (문자열 형태)
        """
        nRead = self.ard.in_waiting  # 버퍼에 있는 읽을 데이터 크기 확인
        if nRead > 0:
            btRead = self.ard.read(nRead)  # Serial 포트에서 데이터 읽기
            sRead = btRead.decode()  # 바이트를 문자열로 디코딩
            return sRead
        else:
            return ''  # 읽을 데이터가 없으면 빈 문자열 반환

    def clearSerial(self):
        """
        Serial 포트 버퍼를 비우는 메소드
        """
        PythonHub.waitSerial()  # 정적 메소드 waitSerial() 호출
        self.readSerial()  # Serial 포트에서 데이터 읽기 (버퍼 비우기)
    
    def talk(self, sCmd):
        """
        Serial 통신을 통해 데이터를 보내는 메소드
    
        Parameters:
        - sCmd (str): 보낼 데이터로 문자열 형태여야 함
    
        Returns:
        - int: 쓰여진 바이트 수
        """
        return self.writeSerial(sCmd + '\n')  # 개행 문자(\n)를 추가하여 데이터 보내기
    
    def listen(self):
        """
        Serial 통신을 통해 데이터를 받는 메소드
    
        Returns:
        - str: 받은 데이터 (문자열 형태)
        """
        PythonHub.waitSerial()  # 정적 메소드 waitSerial() 호출
        sRead = self.readSerial()  # Serial 포트에서 데이터 읽기
        return sRead.strip()  # 양 끝의 공백 제거 후 반환
    
    def talkListen(self, sCmd):
        """
        Serial 통신을 통해 데이터를 보내고 받는 메소드
    
        Parameters:
        - sCmd (str): 보낼 데이터로 문자열 형태여야 함
    
        Returns:
        - str: 받은 데이터 (문자열 형태)
        """
        self.talk(sCmd)  # 데이터 보내기
        return self.listen()  # 데이터 받기
        
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # DB 메소드
    def connectDb(self):
        self.conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='2023', port='5432') # DB connection 얻기
        self.cur = self.conn.cursor() # connection의 cursor(커서)
        
    def closeDb(self):
        self.cur.close()
        self.conn.close()
        
    def writeDb(self, cmd): # DB에 명령어 cmd 쓰기
        sCmd = str(cmd) # string으로 type casting
        self.cur.execute(sCmd) # cursor에 명령어(SQL) 실행
        self.conn.commit() # connection에 기록하기 -> cursor 명령어를 DB가 실행
           

# =======================================================전압(volt) 메소드 모음 ===============================================================
# =============================================================================================================================================
     # 전압계 메소드 
    def getVolt(self):
        try: # 코드 시도(try)
            sVolt = self.talkListen('get volt')
            volt = float(sVolt) # 문자열 sVolt를 float(double)으로 변경
            return volt
        except: # try 부분에서 에러가 발생한 경우 실행되는 코드
            print('Serial error!')
            return -1
            
    # 행의 갯수를 return
    def countVoltTable(self):
        self.connectDb()
        self.writeDb('SELECT COUNT(*) FROM volt_table')
        nCount = self.cur.fetchone()[0]
        self.closeDb()
        return nCount

    # 하나의 volt값을 DB에 저장
    def insertOneVoltTable(self): # 전압측정값 하나를 DB에 추가
        self.connectDb()
        volt = self.getVolt()
        measTime = time.time()
        if volt>=0:
            self.writeDb(f'INSERT INTO volt_table(meas_time, volt) VALUES({measTime}, {volt})')
            self.closeDb()
            return True
        else: return False

    # DB에 있는 volt_table 측정값 삭제
    def clearVoltTable(self):
        self.connectDb()
        self.writeDb('TRUNCATE volt_table')
        self.closeDb()

    # 전압 측정값을 담은 튜플을 초기화
    def clearVoltTuple(self):
        self.volts = () # 전압 측정값을 담은 튜플; (): 현재 변수를 tuple로 초기화
        self.voltTimes = () # 전압 측정 시간을 담은 tuple(튜플)

    # 전압 튜플에 있는 측정값 출력
    def printVoltTuple(self):
        for (volt, measTime) in zip(self.volts, self.voltTimes)  :
            print(f'volt = {volt} @ time = {time.ctime(measTime)}') ## f: formatted string을 의미; {...} 안을 코드로 인식해 실행 -> 
            #그 결과는 문자열로 반환; ctime(): char time -> 현재 에포크 타임을 보기 편한 문자열 시간으로 변경

    # 튜플에 전압 측정값 삽입
    def addVoltToTuple(self):
        volt = self.getVolt()
        measTime = time.time() # 현재 시간 읽기: 에포크 타임(기원후 시간, epoch time)
        if volt >= 0: # 측정 성공
            self.volts += (volt,) # 원소 하나인 튜플은 마지막에 , 추가
            self.voltTimes += (measTime,)
            return True
        else: return False # 측정 실패

    # delay 주기로 전압 측정값을 샘플링 -> 샘플링 결과는 volts, voltTimes 튜플에 저장
    def sampleVoltTuple(self, nCount, delay): 
        for i in range(nCount):
            self.addVoltToTuple()
            print(self.volts)
            print(self.voltTimes)
            PythonHub.wait(delay)
        
    # volts, voltTimes 튜플을 DB에 저장; volt, voltsTime는 clear
    def saveVoltTupleToTable(self):
        self.connectDb()
        for i in range(len(self.volts)):
            measTime = self.voltTimes[i]
            volt = self.volts[i]
            self.writeDb(f'INSERT INTO volt_table(meas_time, volt) VALUES({measTime}, {volt})')
        self.closeDb()
        self.clearVoltTuple()

    # DB에서 정보를 가져와서 volts, voltTimes 튜플에 추가
    def loadVoltTupleFromTable(self): 
        self.connectDb()
        self.writeDb('SELECT meas_time, volt FROM volt_table')
        result = self.cur.fetchall()
        print(result)
        for voltTime, volt in result:
            self.voltTimes += (voltTime,)
            self.volts += (volt,) # 원소 하나인 튜플은 마지막에 , 추가
        print(self.volts)
        print(self.voltTimes)
        self.closeDb()

    #전압의 평균
    def getVoltMean(self):
        return stat.mean(self.volts)
    # 전압의 표준편차
    def getVoltStdev(self):
        return stat.stdev(self.volts)   
    # 전압의 그래프
    def plotVoltTuple(self):
        plt.plot(self.voltTimes, self.volts)
        plt.show()

    # 전압 측정값을 html형식으로 나타냄
    def writeHtmlVoltTuple(self):
        html = '<table width="100%" border="1"><thead><tr><th>번호</th><th>전압 측정값</th><th>측정 일시</th></tr></thead>'
        i = 1
        for(volt, voltTime) in zip(self.volts, self.voltTimes):
            html += f'<tr><td>{i}</td><td>{volt} V</td><td>{time.ctime(voltTime)}</td></tr>'
            i += 1
        html += '</table>'
        return html
    # 전압의 평균, 분산, 표준편차 값들을 html형식으로 출력
    def describeVoltTable(self):
        self.connectDb()
        self.writeDb("SELECT volt FROM volt_table")
        result = self.cur.fetchall()

        df = pd.DataFrame(result, columns=['volt'])
        self.closeDb()    
        # self.voltcount = df.shape[0]
        # self.voltmedian = df['volt'].median().item()
        self.voltmean = round(df['volt'].mean().item(), 2)
        self.voltstd = round(df['volt'].std().item(), 2)
        self.voltvar = round(df['volt'].var().item(), 2)
        
        html = f'<div><p>평균(mean): {self.voltmean}, 분산(var): {self.voltvar}, 표준편차(Stdev): {self.voltstd}</p></div>'
        return html
    
# =======================================================조도(light) 메소드 모음 ===============================================================
# =============================================================================================================================================
    # 조도 센서 밝기
    def getLight(self):
        try:
            sLight = self.talkListen('get light')
            Light = str(sLight)
            return Light
        except:
            print('Serial error!')
            return -1

    # 조도 센서 밝기 수치
    def getLightStep(self):
        try:
            nLightStep = self.talkListen('get lightstep')
            lightStep = float(nLightStep)
            return lightStep
        except:
            print('Serial error!')
            return -1
    
    # 조도 테이블의 행의 갯수
    def countLightTable(self):
        self.connectDb()
        self.writeDb('SELECT COUNT(*) FROM light_table')
        nCount = self.cur.fetchone()[0]
        self.closeDb()
        return nCount

    # 전압측정값 하나를 DB에 추가
    def insertOneLightTable(self): 
        self.connectDb()
        light = self.getLight()
        lightStep = self.getLightStep()
        measTime = time.time()
        if lightStep>=0:
            self.writeDb(f"INSERT INTO light_table(meas_time, light, light_step) VALUES({measTime}, '{light}', {lightStep})")
            self.closeDb()
            return True
        else: return False

    # DB에 저장된 전압 측정값을 삭제
    def clearLightTable(self): 
        self.connectDb()
        self.writeDb('TRUNCATE light_table')
        self.closeDb()
    
    # 조도 측정값을 저장하고 있는 튜플을 초기화
    def clearLightTuple(self):
        self.lights = ()
        self.lightSteps = ()
        self.lightTimes = ()

    # 조도 튜플에 측정값 추가
    def addLightToTuple(self):
        light = self.getLight()
        lightStep = self.getLightStep()
        measTime = time.time() # 현재 시간 읽기: 에포크 타임(기원후 시간, epoch time)
        self.lights += (light,)
        self.lightSteps += (lightStep,)
        self.lightTimes += (measTime,)
        return True

    # 횟수를 지정해주어 light값을 측정
    def sampleLightTuple(self, nCount, delay):
        for i in range(nCount):
            self.addLightToTuple()
            print(self.lightTimes)
            print(self.lights)
            print(self.lightSteps)
            PythonHub.wait(delay)

    # 위에 나온 측정값을 DB(light_table)에 저장
    def saveLightTupleIntoTable(self):
        self.connectDb()
        for (light, lightStep, measTime) in zip(self.lights, self.lightSteps, self.lightTimes):
            self.writeDb(f"INSERT INTO light_table(meas_time, light, light_step) VALUES({measTime}, '{light}', {lightStep})")
            self.clearLightTuple()
        return True
        self.closeDb()

    # DB에 저장된 조도 측정값들을 가져옴
    def loadLightTupleFromTable(self):
        self.connectDb()
        self.writeDb('SELECT meas_time, light, light_step FROM light_table')
        result = self.cur.fetchall()
        for meas_time, light, light_step in result:
            self.lights += (light,)
            self.lightSteps += (light_step,)
            self.lightTimes += (meas_time,)
        print(self.lights)
        print(self.lightSteps)
        print(self.lightTimes)
        self.closeDb()

    # light의 평균
    def getLightMean(self):
        return stat.mean(self.lightSteps)
    # light의 표준편차
    def getLightStdev(self):
        return stat.stdev(self.lightSteps)
    # light의 그래프
    def plotLightTuple(self):
        plt.plot(self.lightTimes, self.lightSteps)
        plt.show()

    # 조도 튜플에 저장되어있는 측정값을 html형식으로 출력
    def writeHtmlLightTuple(self):
        html = '<table width="100%" border="1"><thead><tr><th>번호</th><th>조도 측정 단계</th><th>조도 측정값</th><th>측정 일시</th></tr></thead>'
        i = 1
        for(light, lightStep, lightTime) in zip(self.lights, self.lightSteps, self.lightTimes):
            html += f'<tr><td>{i}</td><td>{light}</td><td>{lightStep}</td><td>{time.ctime(lightTime)}</td></tr>'
            i += 1
        html += '</table>'
        return html

    # 조도 수치 측정값을 평균, 분산, 표준편차를 html로 출력
    def describeLightTable(self):
        self.connectDb()
        self.writeDb("SELECT light_step FROM light_table")
        result = self.cur.fetchall()

        df = pd.DataFrame(result, columns = ['light_step'])
        self.closeDb()
        # self.lightcount = df.shape[0]
        # self.lightmedian = df['light_step'].median().item()
        self.lightmean = round(df['light_step'].mean().item(), 2)
        self.lightstd = round(df['light_step'].std().item(), 2)
        self.lightvar = round(df['light_step'].var().item(), 2) 
        html = f'<div><p>평균(mean): {self.lightmean}, 분산(var): {self.lightvar}, 표준편차(Stdev): {self.lightstd}</p></div>'
        return html
    
# =======================================================모터(servo 모터) 메소드 모음 ===============================================================
# =================================================================================================================================================
    def setServoMove(self, ang): # ang만큼 각도 회전
        try:
            nAng = int(ang) # 변수 ang -> int로 변경(type casting)
            sAng = str(nAng) # int nAng =-> 문자열로 변경
            self.talk('set servo ' + sAng)
        except:
            print('각도 설정 류')

# =======================================================LED 메소드 모음 ===========================================================================
# =================================================================================================================================================
    def setLedColor(self, color):
        try:
            self.talk('set led ' + color)
        except:
            print('색깔 지정 오류')

# =======================================================부터(buzzer) 메소드 모음===================================================================
# =================================================================================================================================================
    def setBuzzerNote(self, note, delay):
        try:
            sDelay = str(delay)
            self.talk('set buzzer ' + note + ' ' + sDelay)
        except:
            print('음계 지정 오류')