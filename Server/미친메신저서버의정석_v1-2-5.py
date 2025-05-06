#집가고싶다 Inc.
#미친메신저서버의정석

#미친메신저서버의정석 v1.2.5
#AMS102

#패키지
from tkinter import *
import tkinter.ttk as ttk
import socket
import threading
import datetime
import time
import os

#건드리면 안되는 변수
HOST = "0.0.0.0"
clients = [] #클라이언트소켓모음
users = [] #클라이언트이름 (유저)
usersSelect = ["EVERYONE"] #서버메시지 전송시 사용
clientsInfo = {} #클라이언트소켓 => 클라이언트정보
usersClients = {} #클라이언트이름 => 클라이언트소켓
clientsAdr = {} #클라이언트소켓 => 클라이언트주소
filePath = os.path.dirname(os.path.abspath(__file__)) #파이썬파일경로
txtFilePath = os.path.join(filePath, "log.txt") #log.txt파일 경로

#사용자 정의 변수 (프로그램 내에서 변경 가능)
# PORT = 888 #프로그램 내에서 포트 지정 가능
# displayIP = ""
# maxUsers = 0 #최대 서버 인원

#개발 버전 변수
version = "AMS102"
displayVersion = "1.2.5"

#서버 실행
def start():
    global txtOut
    if logOut.get() == 1:
        txtOut = True
    else:
        txtOut = False
    displayIP = displayIPentry.get()
    try:
        PORT = int(portEntry.get())
    except:
        log("SYSTEM", "서버 포트를 정수형으로 입력해주세요.")
        return
    try:
        maxUsers = int(maxUsersEntry.get())
    except:
        log("SYSTEM", "서버 최대 인원을 정수형으로 입력해주세요.")
        return

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(maxUsers)
    except Exception as e:
        log("SYSTEM", e)
        return

    log("SYSTEM", f"{displayIP}:{PORT}에서 서버를 실행했습니다.")

    while True:
        clientSocket, adr = serverSocket.accept()
        communicating = threading.Thread(target=communicate, args=(clientSocket, adr))
        communicating.start()

def communicate(clientSocket, adr):
    log(adr, "서버에 접속했습니다.")
    info, name = check(clientSocket, adr)
    if info == "name" and name == "duplicate":
        clientSocket.close()
        log(adr, "서버에 해당 유저의 이름을 가진 유저가 이미 있기에 서버와 연결을 끊었습니다.")
        return
    log(adr, f"서버의 인증과정을 통과하였습니다. (이름 : {name}, 클라이언트정보 : {info})")
    
    clients.append(clientSocket) #클라이언트소켓에 유저소켓 추가
    clientsInfo[clientSocket] = info #클라이언트소켓에 유저정보 추가
    users.append(name) #유저 추가
    usersClients[name] = clientSocket #클라이언트이름에 유저소켓 추가
    usersList.insert(END, name) #서버 내에 유저목록에 유저 추가
    usersSelect.append(name) #서버내 메시지전송대상에 유저 추가
    messageUsersSelect["values"] = usersSelect #메시지전송대상 다시 로드
    clientsAdr[clientSocket] = adr #유저소켓에 유저주소 추가

    #미친메신저의정석 v1.2

    if info == "AM102":
        time.sleep(3)
        everyone(f"{name}님이 서버에 접속했습니다.")
        
        while True:
            try:
                rcvdMsg = receive(clientSocket, adr)
                
                if not rcvdMsg:
                    break
                elif rcvdMsg == "!users":
                    send(clientSocket, adr, f"\n--현재 온라인 클라이언트--\n{users}\n>>> ")
                else:
                    everyone(f"[{name}] : {rcvdMsg}")
            except Exception as e:
                log("SYSTEM", e)
                break
        
        log(adr, "서버와 연결이 끊겼습니다.")
        everyone(f"{name}님이 서버와 연결이 끊겼습니다.")
    
    #미친메신저의정석 GUI 프로토타입

    elif info == "AMGP":
        everyone(f"{name}님이 서버에 접속했습니다.")
        
        while True:
            try:
                rcvdMsg = receive(clientSocket, adr)
                
                if not rcvdMsg:
                    break
                elif rcvdMsg == "!users":
                    send(clientSocket, adr, f"\n--현재 온라인 클라이언트--\n{users}")
                else:
                    everyone(f"[{name}] : {rcvdMsg}")
            except Exception as e:
                log("SYSTEM", e)
                break
        
        log(adr, "서버와 연결이 끊겼습니다.")
        everyone(f"{name}님이 서버와 연결이 끊겼습니다.")

    #지원안함

    else:
        #개발자가 귀찮으면 생기는 일
        send(clientSocket, adr, "\n지원되지 않는 클라이언트 같습니다.\nhttps://www.iwanttogohome.net/ 에서 최신 클라이언트를 다운로드하세요.\n\n3초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, adr, "2초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, adr, "1초후에 연결을 끊습니다.")
        time.sleep(1)
        log(adr, "서버의 인증과정을 실패하여 연결을 끊었습니다.")
    
    clients.remove(clientSocket)
    clientsInfo.pop(clientSocket)
    users.remove(name)
    usersClients.pop(name)
    deleteUsersListIndex(name)
    usersSelect.remove(name)
    messageUsersSelect["values"] = usersSelect
    clientsAdr.pop(clientSocket)
    clientSocket.close()

#서버 내 메시지 전송
def sendMessage():
    user = messageUsersSelect.get()
    if messageNameVar.get() == 1:
        name = True
    else:
        name = False
    if user == "EVERYONE":
        if name == True:
            everyone(f"[SERVER] : {messageText.get("1.0", END).strip()}")
        else:
            everyone(messageText.get("1.0", END).strip())
    else:
        try:
            clientSocket = usersClients[messageUsersSelect.get()]
            adr = clientsAdr[clientSocket]

            if clientsInfo[clientSocket] == "AM102":
                if name == True:
                    send(clientSocket, adr, f"[SERVER] : {messageText.get("1.0", END).strip()}\n>>> ")
                else:
                    send(clientSocket, adr, f"{messageText.get("1.0", END).strip()}\n>>> ")
            elif clientsInfo[clientSocket] == "AMGP":
                if name == True:
                    send(clientSocket, adr, f"[SERVER] : {messageText.get("1.0", END).strip()}")
                else:
                    send(clientSocket, adr, messageText.get("1.0", END).strip())
            else:
                if name == True:
                    send(clientSocket, adr, f"[SERVER] : {messageText.get("1.0", END).strip()}")
                else:
                    send(clientSocket, adr, messageText.get("1.0", END).strip())
        except Exception as e:
            log("SYSTEM", e)
    messageText.delete("1.0", END)
    

def check(clientSocket, adr):
    send(clientSocket, adr, "info?")
    info = receive(clientSocket, adr)
    send(clientSocket, adr, "name?")
    name = receive(clientSocket, adr)

    if name in users:
        log("SYSTEM", "중복된 이름을 가진 유저가 접속했습니다. 해당 유저의 연결을 끊습니다.")
        send(clientSocket, adr, f"\"{name}\"이라는 이름을 가진 유저가 이미 있습니다.\n다른 이름을 사용해주세요.\n\n")
        send(clientSocket, adr, "3초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, adr, "2초후에 연결을 끊습니다.")
        time.sleep(1)
        send(clientSocket, adr, "1초후에 연결을 끊습니다.")
        time.sleep(1)

        return "name", "duplicate"

    return info, name

#로그 출력
def log(adr, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logList.insert(END, f"[{timestamp}] ({adr}) {message}")
    logList.see(END)
    if txtOut == True:
        with open(txtFilePath, "a", encoding="utf-8") as logFile:
            logFile.write(f"[{timestamp}] ({adr}) {message}\n")

def startServer():
    server = threading.Thread(target=start)
    server.start()

def send(clientSocket, adr, message):
    try:
        clientSocket.sendall(message.encode())
        log(f"SERVER => {adr}", f": \"{message}\"")
    except Exception as e:
        log("SYSTEM", e)

def receive(clientSocket, adr):
    try:
        rcvdMsg = clientSocket.recv(1024).decode()
        log(adr, f": \"{rcvdMsg}\"")
        return rcvdMsg
    except Exception as e:
        log("SYSTEM", e)

def everyone(message):
    log("SERVER => EVERYONE", f": \"{message}\"")
    for client in clients:
        try:
            if clientsInfo[client] == "AMGP": #미친메신저의정석 GUI 프로토타입 전송방식
                client.sendall(message.encode())
            elif clientsInfo[client] == "AM102": #미친메신저의정석 v1.2 전송방식
                client.sendall(f"{message}\n>>> ".encode())
            else: #나머지 (??)
                client.sendall(message.encode())
        except Exception as e:
            log("SYSTEM", e)

def deleteUsersListIndex(name):
    listCount = usersList.size()
    for i in range(listCount):
        if usersList.get(i) == name:
            usersList.delete(i)
            break

#티킨터 세팅
root = Tk()
root.geometry("640x480")
root.title(f"미친메신저서버의정석 v{displayVersion}")

#상?표
title = Label(root, text=f"집가고싶다 Inc.\n미친메신저서버의정석 v{displayVersion}", justify=LEFT)
title.grid(row=0, column=0, sticky=N+W)

#서버 설정
settingFrame = LabelFrame(root, text="서버 설정", relief="solid", bd=1)
settingFrame.grid(row=1, column=0)

#표시 서버 주소 입력
putDisplayIPlabel = Label(settingFrame, text="표시 서버 주소 :")
putDisplayIPlabel.grid(row=0, column=0, sticky=E)

displayIPentry = Entry(settingFrame)
displayIPentry.grid(row=0, column=1)

#서버 포트 입력
putPortLabel = Label(settingFrame, text="서버 포트 :")
putPortLabel.grid(row=1, column=0, sticky=E)

portEntry = Entry(settingFrame)
portEntry.grid(row=1, column=1)

#서버 최대 인원 입력
putMaxUsersLabel = Label(settingFrame, text="서버 최대 인원 :")
putMaxUsersLabel.grid(row=2, column=0, sticky=E)

maxUsersEntry = Entry(settingFrame)
maxUsersEntry.grid(row=2, column=1)

#log.txt 로그 출력 여부
logOut = IntVar()
logOutChkBtn = Checkbutton(settingFrame, text="log.txt 로그 출력", variable=logOut)
logOutChkBtn.select()
logOutChkBtn.grid(row=3, column=0, columnspan=2, sticky=W)

#서버 실행 버튼
startBtn = Button(settingFrame, text="서버 실행", command=startServer)
startBtn.grid(row=4, column=1, sticky=E)

#로그
logFrame = LabelFrame(root, text="로그", relief="solid", bd=1)
logFrame.grid(row=0, column=1, rowspan=2, sticky=E+W)

logList = Listbox(logFrame, selectmode="extended", width=35, height=10)
logScrollbar = Scrollbar(logFrame, orient="vertical", command=logList.yview)
logList.config(yscrollcommand=logScrollbar.set)

logList.grid(row=0, column=0, sticky=E+W)
logScrollbar.grid(row=0, column=1, sticky=N+S)

#유저
usersFrame = LabelFrame(root, text="유저", relief="solid", bd=1)
usersFrame.grid(row=2, column=1, sticky=E+W)

usersList = Listbox(usersFrame, selectmode="extended", width=35, height=5)
usersScrollbar = Scrollbar(usersFrame, orient="vertical", command=usersList.yview)
usersList.config(yscrollcommand=usersScrollbar.set)

usersList.grid(row=0, column=0, sticky=E+S)
usersScrollbar.grid(row=0, column=1, sticky=N+S)

#메시지
messageFrame = LabelFrame(root, text="메시지", relief="solid", bd=1)
messageFrame.grid(row=3, column=1, sticky=E+W)

messageUsersSelectLabel = Label(messageFrame, text="전송 상대 :")
messageUsersSelect = ttk.Combobox(messageFrame, height=5, values=usersSelect, state="readonly")
messageTextLabel = Label(messageFrame, text="메시지 :")
messageText = Text(messageFrame, width=30, height=5)
messageNameVar = IntVar()
messageNameChkbtn = Checkbutton(messageFrame, text="메시지 앞 이름", variable=messageNameVar)
messageSendButton = Button(messageFrame, text="전송", command=sendMessage)

messageUsersSelectLabel.grid(row=0, column=0, sticky=E)
messageUsersSelect.grid(row=0, column=1, sticky=W)
messageTextLabel.grid(row=1, column=0, sticky=N+E)
messageText.grid(row=1, column=1, sticky=W)
messageNameChkbtn.grid(row=2, column=0, columnspan=2, sticky=W)
messageSendButton.grid(row=3, column=2, sticky=E)

root.mainloop()
