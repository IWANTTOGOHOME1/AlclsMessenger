#집가고싶다 inc. 미친메신저의정석 클라이언트 1세대
#특정 인물들만 이해할수 있는 미친 메신저

#미친메신저의정석 1세대 v1.2.3

#v1.2.2 패치노트
#버전정보 깔끔하게 변경
#오류 발생시 프로그램이 종료되지 않는 버그 수정
#이름변경
#메뉴의 옵션명 변경
#메뉴 설정 완료시 화면 초기화
#로고 애니메이션 추가

#v1.2.3 패치노트
#유저목록 표시기능 추가
#버전정보 형식 변경 (버전1.~~ => v1.~~)
#난해한 변수명 정상화 및 가독성 강화
#주석 추가
#프로그램 가독성 약간 상승

#패키지
import socket
import threading
import sys
import time
import os

#개발 버전 변수
version = "AM102"
displayVersion = "1.2.3"

#건드리면 안되는 변수
logo = [
"⠀⠀⣀⠀⢀⡀⢀⡀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⣀⢀⡀⠀⠀⠀⠀",
"⠀⠀⢹⡆⡘⣧⢠⠁⣠⠂⣄⢸⡇⢠⠔⢤⠀⡤⠢⡄⢰⡤⢢⡄⢢⡀⢠⠔⣄⠀⠀⠈⠀⣿⠀⠃⣠⠂⣄⠀",
"⠀⠀⠈⣧⠁⢹⡌⠀⣯⠀⢉⢸⡇⢸⡄⠀⠸⡇⠀⡟⢸⡇⢸⡇⢸⡇⢿⠀⢈⠀⠀⠀⠀⣿⠀⠐⡧⠀⡿⠀",
"⠀⠀⠀⠁⠀⠈⠁⠀⠈⠉⠁⠈⠁⠀⠉⠉⠀⠉⠈⠀⠈⠉⠈⠁⠉⠁⠀⠉⠁⠀⠀⠀⠈⠉⠁⠀⠈⠈⠁⠀",
"⠀⠀⠀⠀⢶⡄⠀⠀⢰⡖⠀⠀⠀⠀⠀⠐⣶⠀⠀⠀⠀⠀⠀⠀⠀⡶⣦⠀⠀⢠⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⡜⠈⣷⠀⠀⢸⡇⠀⣴⠉⠹⠆⢈⣿⠀⣴⡉⠹⠀⠀⠀⠀⡇⢹⣆⠀⠆⣿⡇⢀⡾⠉⢳⡄⢴⡉⠹⠀⣾⡉⠹⠀⣴⠉⠹⣆⠈⣿⠊⢹⡦⠀⣶⠉⢹⡇⢠⡎⠉⣶⠀⢹⡗⠻⠀⠀⠀",
"⠀⠀⢰⠉⠉⢹⣧⠀⢸⡇⠐⣿⡀⠀⡀⠠⣿⠀⡌⠙⢷⠀⠀⠀⠀⡇⠀⢿⡜⠀⢿⡇⠸⣧⠁⠁⡁⣈⠙⢳⠄⡌⠙⢷⠀⣿⠁⠉⡀⠀⣿⠀⢸⡯⠀⣽⠂⠚⠁⢸⣏⠈⠀⠁⢸⡇⠀⠀⠀⠀",
"⠀⠀⠉⠀⠀⠈⠉⠁⠈⠉⠀⠈⠉⠈⠀⠈⠉⠀⠉⠐⠉⠀⠀⠀⠀⠉⠀⠈⠀⠀⠉⠁⠀⠈⠁⠈⠀⠈⠐⠈⠀⠉⠀⠁⠀⠈⠉⠈⠀⠀⠉⠀⠈⠉⠀⣝⠉⠋⡿⠀⠉⠁⠉⠀⠉⠁⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
]

#연결 아이피 설정
while True:
    decision = input("\n[1] 메인 서버로 접속\n[2] 외부 서버로 접속\n> ")
    if decision == "1":
        HOST = "messenger.iwanttogohome.net"
        break
    elif decision == "2":
        HOST = input("\n접속할 서버의 주소를 입력하세요.\n> ")
        break
    else:
        print("\n잘못된 값을 입력했습니다.\n 다시 입력하세요.")

#포트 설정
while True:
    decision = input("\n[1] 메인 서버포트로 접속\n[2] 개발 서버포트로 접속 (서버가 열려있지 않을수도 있음)\n[3] 외부 서버포트로 접속\n> ")
    if decision == "1":
        PORT = 887
        break
    elif decision == "2":
        PORT = 888
        break
    elif decision == "3":
        while True:
            try:
                PORT = int(input("\n접속할 서버의 포트를 입력하세요.\n> "))
                break
            except:
                print("\n값을 정수형으로 입력해주세요.")
        break
    else:
        print("\n잘못된 값을 입력했습니다.\n다시 입력하세요.")

name = input("\n이름을 입력하세요.\n> ") #클라이언트 이름 설정

#화면 초기화 함수
def clear():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

#서버 주 통신 함수
def receive():
    while True:
        rcvdMsg = clientSocket.recv(1024).decode()
        if rcvdMsg == "name?": #서버가 이름 정보 물어보면?
            clientSocket.sendall(name.encode())
        elif rcvdMsg == "info?": #서버가 버전 정보 물어보면?
            clientSocket.sendall(version.encode())
        else:
            if not rcvdMsg: #서버가 닫히면
                print("\n\n서버가 닫혔거나 네트워크에 문제가 있는 것 같습니다.", file=sys.stderr)
                time.sleep(1)
                os._exit(0) #나감
            print(f"\r{rcvdMsg}", end="")

receiving = threading.Thread(target=receive)

#수신 시작 세팅
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    clientSocket.connect((HOST, PORT))
except Exception as e: #서버 연결 안되면
    print(f"\n서버가 열려있지 않은것 같습니다.\n오류 로그 : {e}\n", file=sys.stderr)
    time.sleep(1)
    sys.exit(1)

receiving.start()

clear() #초기화 해주고 시작
for i in logo: #로고 출력
    time.sleep(0.1)
    print(i)
time.sleep(1)
print(f"\n집가고싶다 inc.\n미친메신저의정석 1세대 v{displayVersion}\n\n서버주소 : {HOST}\n서버포트 : {PORT}\n이 클라이언트의 이름 : {name}\n\n!exit를 입력하면 프로그램을 종료합니다.\n!users를 입력하면 서버에 연결되어있는 유저 정보를 얻을수 있습니다.\n\n", end="")

while True:
    message=input()
    if message == "!exit":
        #노가다
        print("\n3초후에 프로그램을 종료합니다.", end = "")
        time.sleep(1)
        print("\r2초후에 프로그램을 종료합니다.", end = "")
        time.sleep(1)
        print("\r1초후에 프로그램을 종료합니다.", end = "")
        time.sleep(1)
        os._exit(0) #강종
    else:
        clientSocket.sendall(message.encode()) #메시지 전송
