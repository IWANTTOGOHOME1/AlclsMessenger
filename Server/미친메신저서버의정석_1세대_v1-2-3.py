#집가고싶다 Inc.
#미친메신저서버의정석 1세대

#미친메신저서버의정석 1세대 v1.2.3

#패키지
import socket
import threading
import datetime
import time

#건드리면 안되는 변수
HOST = "0.0.0.0"
clients = []
users = []
clientsInfo = {}

#사용자 정의 변수
PORT = 887
ip = "Unknown" #편의용
maxUsers = 50

#개발 버전 변수
version = "AMS102"
displayVersion = "1.2.3"
# availableClientVersion = ["AM102", "COS202", "AMGP"] #미친메신저의정석v1.2, CatOS2, 미친메신저의정석GUI프로토타입 <=필요없어짐

#클라이언트의 정보 확인 함수
def check(item, clientSocket, adr):
    if item == "INFO": #클라이언트 정보 확인
        send(clientSocket, "info?")
        rcvdMsg = clientSocket.recv(1024).decode()
        log(adr, f": \"{rcvdMsg}\"")
        return rcvdMsg
    elif item == "NAME": #클라이언트 이름 확인
        send(clientSocket, "name?")
        rcvdMsg = clientSocket.recv(1024).decode()
        log(adr, f": \"{rcvdMsg}\"")
        return rcvdMsg

#특정 클라이언트에 메시지 전송
def send(clientSocket, message):
    try:
        clientSocket.sendall(message.encode())
        log("SERVER", f": \"{message}\"")
    except Exception as e:
        log("SYSTEM", e)

#전체 클라이언트에 메시지 전송
def everyone(message):
    for client in clients:
        try:
            if clientsInfo[client] == "AMGP": #미친메신저의정석 GUI 1세대 프로토타입 전송방식
                client.sendall(message.encode())
            elif clientsInfo[client] == "AM102": #미친메신저의정석 v1.2 전송방식
                client.sendall(f"{message}\n>>> ".encode())
            else: #나머지 (??)
                client.sendall(message.encode())
        except Exception as e:
            log("SYSTEM", e)        
    log("SERVER", f": \"{message}\"")

#서버 txt파일 및 로그 출력
def log(adr, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #날짜&시간 입력
    print(f"\r[{timestamp}] ({adr}) {message}")
    with open("log.txt", "a", encoding="utf-8") as logFile:
        logFile.write(f"[{timestamp}] ({adr}) {message}\n")

def communication(clientSocket, adr):
    log(adr, "서버에 접속했습니다.")
    info = check("INFO", clientSocket, adr) #클라이언트의 정보 얻기
        
    #미친메신저의정석 1세대 v1.2

    if info == "AM102": #통신 코드
        name = check("NAME", clientSocket, adr) #클라이언트의 이름 얻기
        log(adr, f"서버의 인증과정을 통과하였습니다. (이름 : {name}, 클라이언트정보 : {info})")
        clients.append(clientSocket) #클라이언트들에 추가
        clientsInfo[clientSocket] = info
        users.append(name) #유저에 추가
        time.sleep(3) #클라이언트 애니메이션 출력 대기 시간 (보험)
        everyone(f"{name}님이 서버에 접속했습니다.")
        while True:
            try:
                rcvdMsg = clientSocket.recv(1024).decode()
                if not rcvdMsg: #갑자기 나가면
                    break
                log(adr, f": \"{rcvdMsg}\"")
                if rcvdMsg == "!users": #유저정보 요구
                    send(clientSocket, f"\n--현재 온라인 클라이언트--\n{users}\n>>> ")
                else:
                    everyone(f"[{name}] : {rcvdMsg}")
            except Exception as e:
                log("SYSTEM", e)
                break
        log(adr, "서버와 연결이 끊겼습니다.")
        everyone(f"{name}님이 서버와 연결이 끊겼습니다.")
        clients.remove(clientSocket) #클라이언트 목록에서 제거
        clientsInfo.pop(clientSocket)
        users.remove(name) #유저 목록에서 제거
        clientSocket.close() #통신 단절
    
    #미친메신저의정석 GUI 1세대 프로토타입

    elif info == "AMGP":
        name = check("NAME", clientSocket, adr) #클라이언트의 이름 얻기
        log(adr, f"서버의 인증과정을 통과하였습니다. (이름 : {name}, 클라이언트정보 : {info})")
        clients.append(clientSocket) #클라이언트들에 추가
        clientsInfo[clientSocket] = info
        users.append(name) #유저에 추가
        everyone(f"{name}님이 서버에 접속했습니다.")
        while True:
            try:
                rcvdMsg = clientSocket.recv(1024).decode()
                if not rcvdMsg: #갑자기 나가면
                    break
                log(adr, f": \"{rcvdMsg}\"")
                if rcvdMsg == "!users": #유저정보 요구
                    send(clientSocket, f"\n--현재 온라인 클라이언트--\n{users}")
                else:
                    everyone(f"[{name}] : {rcvdMsg}")
            except Exception as e:
                log("SYSTEM", e)
                break
        log(adr, "서버와 연결이 끊겼습니다.")
        everyone(f"{name}님이 서버와 연결이 끊겼습니다.")
        clients.remove(clientSocket) #클라이언트 목록에서 제거
        clientsInfo.pop(clientSocket)
        users.remove(name) #유저 목록에서 제거
        clientSocket.close() #통신 단절

    else: #빌드업 실패 시
        #개발자가 귀찮으면 생기는 일
        send(clientSocket, "\n지원되지 않는 클라이언트 같습니다.\n최신 클라이언트를 다운로드하세요.\n\n3초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, "2초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, "1초후에 연결을 끊습니다.")
        time.sleep(1)
        log(adr, "서버의 인증과정을 실패하여 연결을 끊었습니다.")
        clientSocket.close() #통신 단절

#프로그램 시작 세팅
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(maxUsers)

#서버 시작로그 출력
print(f"\n집가고싶다 Inc.\n미친메신저서버의정석 1세대 v{displayVersion}\n\n서버주소 : {ip}\n서버포트 : {PORT}\n서버 최대 인원 : {maxUsers}\n\n", end="")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("log.txt", "a", encoding="utf-8") as logFile:
    logFile.write(f"[{timestamp}] (SYSTEM) {ip}:{PORT}에서 서버를 시작했습니다.\n")

#유저 대기 (항상 실행됨)
while True:
    clientSocket, adr=serverSocket.accept()
    communicationing = threading.Thread(target=communication, args=(clientSocket, adr))
    communicationing.start()
