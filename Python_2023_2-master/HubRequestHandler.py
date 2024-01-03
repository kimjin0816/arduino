from http.server import SimpleHTTPRequestHandler
import time
from urllib import parse

class HubRequestHandler(SimpleHTTPRequestHandler): # SimpleHTTPRequestHandler를 상속받아 HubRequestHandler 클래스를 구현
    # 각 해당하는 기능에 대한 경로 지정
    def do_GET(self):
        print(self.path)
        result = parse.urlsplit(self.path)
        if result.path == '/': self.writeHome() # 홈
        elif result.path == '/meas_one_volt': self.writeMeasOneVolt()
        elif result.path == '/sample_volt': self.writeSampleVolt(result.query)
        elif result.path == '/meas_one_light': self.writeMeasOneLight()
        elif result.path == '/meas_one_light' : self.writeLight()
        elif result.path == '/sample_light': self.writeSampleLight(result.query)
        elif result.path == '/servo_move_0' : self.writeServoMove(0)
        elif result.path == '/servo_move_90' : self.writeServoMove(90)
        elif result.path == '/servo_move_180' : self.writeServoMove(180)
        elif result.path == '/servo_move' : self.writeServoAngMove(result.query)
        elif result.path == '/led' : self.writeLed(result.query)
        elif result.path == '/buzzer' : self.writeBuzzer(result.query)
        else: result.writeNotFound() # 페이지가 없음

# =======================================================html 기본 형식 ======================================================================
# ============================================================================================================================================
    # response의 header
    def writeHead(self, nStatus): 
        self.send_response(nStatus)
        self.send_header('content-type', 'text/html') # 속성(attribute), 값 순으로 입력
        self.end_headers()

    # html작성
    def writeHtml(self, html):
        self.wfile.write(html.encode()) # html(유니코드) -> 바이트로 변경(encode() 함수 역할)

    # 페이지의 오류 발생시 출력
    def writeNotFound(self):
        self.writeHead(404) # 404: not found
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>페이지 없음</title>'
        html += '</head><body>'
        html += f'<div><h3>{self.path}에 대한 페이지는 존재하지 않습니다.</h3></div>'
        html += '</body></html>'
        self.writeHtml(html)

    # 홈용 HTML을 쓰기
    def writeHome(self): # 홈용 HTLM을 쓰기
        self.writeHead(200) # 200: 성공
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>Python Web Server</title>'
        html += '</head><body>'
        html += '<div><p><h1>Hello, world!</hl></p>'
        html += '<p><h6>작성자: 조용희</h6></p></div>'
        html += '<div><img src="https://upload.wikimedia.org/wikipedia/commons/e/ee/Mokwon-university.jpg"></div>'
        html += '</body></html>'
        self.writeHtml(html)
# =======================================================전압(volt) 메소드 모음 ===============================================================
# ============================================================================================================================================
    # 전압 한 번 측정
    def writeMeasOneVolt(self):
        self.writeHead(200) # 200: 성공
        nTime = time.time()
        bResult = self.server.gateway.insertOneVoltTable() # gateway == PythonHub의 인스턴스
        if bResult: sResult = '성공'
        else: bResult = '실패'
        nMeasCount = self.server.gateway.countVoltTable()
        self.server.gateway.clearVoltTuple()
        self.server.gateway.loadVoltTupleFromTable()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>전압 한 번 측정</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'
        html += '<button onclick="location.reload();">다시한번 측정</button></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>전압 측정이 {sResult}했습니다.</p>'
        html += f'<p>현재까지 {nMeasCount}번 측정했습니다.</div>'
        html += self.server.gateway.describeVoltTable()
        html += self.server.gateway.writeHtmlVoltTuple()
        html += '</body></html>'
        self.writeHtml(html)
    
    # 전압 샘플링
    def writeSampleVolt(self, qs):
        self.writeHead(200) # 200: 성공
        qdict = parse.parse_qs(qs)
        nCount = int(qdict['count'][0])
        delay = float(qdict['delay'][0])
        nTime = time.time()
        self.server.gateway.clearVoltTuple()
        self.server.gateway.sampleVoltTuple(nCount, delay)
        self.server.gateway.saveVoltTupleToTable()
        nMeasCount = self.server.gateway.countVoltTable()
        self.server.gateway.loadVoltTupleFromTable()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>전압 여러 번 측정</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>전압을 {nCount}번 샘플링했습니다.</p>'
        html += f'<p>현재까지 {nMeasCount}번 측정했습니다.</div>'
        html += self.server.gateway.describeVoltTable()
        html += self.server.gateway.writeHtmlVoltTuple()
        html += '</body></html>'
        self.writeHtml(html)
        
# =======================================================조도(light) 메소드 모음 ===============================================================
# =============================================================================================================================================
    #조도 한 번 측정
    def writeMeasOneLight(self):
        self.writeHead(200) # 200: 성공
        nTime = time.time()
        bResult = self.server.gateway.insertOneLightTable() # gateway == PythonHub의 인스턴스
        if bResult: sResult = '성공'
        else: bResult = '실패'
        nMeasCount = self.server.gateway.countLightTable()
        self.server.gateway.clearLightTuple()
        self.server.gateway.loadLightTupleFromTable()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>조도 한 번 측정</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'
        html += '<button onclick="location.reload();">다시한번 측정</button></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>조도 측정이 {sResult}했습니다.</p>'
        html += f'<p>현재까지 {nMeasCount}번 측정했습니다.</div>'
        html += self.server.gateway.describeLightTable()
        html += self.server.gateway.writeHtmlLightTuple()
        html += '</body></html>'
        self.writeHtml(html)
    
    # 조도 샘플링
    def writeSampleLight(self, qs):
        self.writeHead(200) # 200: 성공
        qdict = parse.parse_qs(qs)
        nCount = int(qdict['count'][0])
        delay = float(qdict['delay'][0])
        nTime = time.time()
        self.server.gateway.clearLightTuple()
        self.server.gateway.sampleLightTuple(nCount, delay)
        self.server.gateway.saveLightTupleIntoTable()
        nMeasCount = self.server.gateway.countLightTable()
        self.server.gateway.loadLightTupleFromTable()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>조도 여러 번 측정</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>조도를 {nCount}번 샘플링했습니다.</p>'
        html += f'<p>현재까지 {nMeasCount}번 측정했습니다.</div>'
        html += self.server.gateway.describeLightTable()
        html += self.server.gateway.writeHtmlLightTuple()
        html += '</body></html>'
        self.writeHtml(html)

# =======================================================모터(servo 모터) 메소드 모음 ===============================================================
# =================================================================================================================================================
    # 모터 이동
    def writeServoMove(self, ang):
        self.writeHead(200) # 200: 성공
        self.server.gateway.setServoMove(ang)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>모터 이동</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'        
        html += f'<div><h5>이동 시작 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>모터를 {ang}도 위치로 이동했습니다</p></div>'
        html += '</body></html>'
        self.writeHtml(html)

    #  모터 자유 이동
    def writeServoAngMove(self, qs):
        self.writeHead(200) # 200: 성공
        qdict = parse.parse_qs(qs)
        nAngle = int(qdict['ang'][0])
        self.server.gateway.setServoMove(nAngle)
        nTime = time.time()
        html = '<html><head>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'        
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>모터 이동</title>'
        html += '</head><body>'
        html += f'<div><h5>이동 시작 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>모터를 {nAngle}도 위치로 이동했습니다</p></div>'
        html += '</body></html>'
        self.writeHtml(html)

# =======================================================LED 메소드 모음 ===========================================================================
# =================================================================================================================================================
    # LED 색깔 출력
    def writeLed(self, qs):
        self.writeHead(200) # 200: 성공
        qdict = parse.parse_qs(qs)
        sColor = str(qdict['color'][0])
        self.server.gateway.setLedColor(sColor)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>LED 점등</title>'
        html += '</head><body>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'        
        html += f'<div><h5>점등 시작 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>점등색은 {sColor}입니다.</p></div>'
        html += '</body></html>'
        self.writeHtml(html)

# =======================================================부터(buzzer) 메소드 모음===================================================================
# =================================================================================================================================================
    # 부저를 연주
    def writeBuzzer(self, qs):
        self.writeHead(200) # 200: 성공
        qdict = parse.parse_qs(qs)
        sNote = str(qdict['note'][0])
        sDelay = str(qdict['delay'][0])
        self.server.gateway.setBuzzerNote(sNote, sDelay)
        nTime = time.time()
        html = '<html><head>'
        html += '<div><button><a href="http://localhost:8080/" style="text-decoration: none; color: black;">홈</a></button>&nbsp&nbsp'        
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>Buzzer</title>'
        html += '</head><body>'
        html += f'<div><h5>부저 시작 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><p>현재는 {sNote}입니다.</p></div>'
        html += '</body></html>'
        self.writeHtml(html)    