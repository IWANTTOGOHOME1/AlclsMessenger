# 집가고싶다 Inc.
# 미친메신저의정석 GUI

# 미친메신저의정석 GUI v1.0.2
# AMG100

# 패키지
from tkinter import *
import tkinter.messagebox as msgbox
import socket
import threading

# 개발 버전 변수
version = "AMG100"
displayVersion = "1.0.2"

communstate = False
misserror = False

# 접속 도움
def connectHelp():
    msgbox.showinfo("도움", "서버 주소 : 접속하려는 서버의 주소(IP)를 입력하세요.\n서버 포트 : 접속하려는 서버의 포트를 입력하세요.\n이름 : 클라이언트의 이름(사용자의 이름)을 입력하세요.\n서버가 없는 경우 : https://www.iwanttogohome.net/ 에서 미친메신저서버의정석을 다운로드하세요.")

# 서버 접속
def connect():
    global name
    global communstate
    global clientSocket
    if communstate == True:
        error("현재 서버에 접속중입니다.\n접속을 해제한 후 시도하세요.")
        return
    HOST = serverAdrEntry.get()
    try:
        PORT = int(serverPortEntry.get())
    except:
        error("서버 포트를 정수형으로 입력하세요.")
        return
    name = clientNameEntry.get()

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((HOST, PORT))
    except Exception as e:
        error(f"서버에 접속하지 못했습니다.\n오류 로그 : {e}")
        return
    communstate = True

    receiving = threading.Thread(target=receive)
    receiving.start()
        

def receive():
    global communstate
    global misserror
    while communstate == True:
        try:
            rcvdMsg = clientSocket.recv(1024).decode()
        except Exception as e:
            if misserror == True:
                misserror = False
                return
            error(f"메시지 수신에서 오류가 발생했습니다.\n서버가 닫혔거나 네트워크에 문제가 있는 것 같습니다.\n오류 로그 : {e}")
            communstate = False
            return
        if rcvdMsg == "name?": #서버가 이름 정보 물어보면?
            clientSocket.sendall(name.encode())
        elif rcvdMsg == "info?": #서버가 버전 정보 물어보면?
            clientSocket.sendall(version.encode())
        else:
            if not rcvdMsg: #서버가 닫히면
                
                error("서버가 닫혔거나 네트워크에 문제가 있는 것 같습니다.")
                communstate = False
                return
            messageOut(rcvdMsg)
            if ringVar.get() == 1:
                msgbox.showinfo("메시지", rcvdMsg)

# 메시지 전송
def send(e=None): # 메시지 입력창에서 엔터 눌렀을때 오류 방지용
    if communstate == True: # 통신중일 때 전송 (오류 방지용)
        clientSocket.sendall(messageInputEntry.get().encode())
        messageInputEntry.delete(0, END)
    else:
        return

# 오류 팝업창 출력
def error(message):
    msgbox.showerror("오류", message)

# 메시지창에 메시지 출력
def messageOut(message):
    messageOutListbox.insert(END, message)
    messageOutListbox.see(END)

# 접속 해제
def disconnect():
    global communstate
    global misserror
    misserror = True
    if communstate == True:
        misserror = True
        communstate = False
        clientSocket.close()
        info("서버와 접속을 해제했습니다.")
    else:
        error("서버에 접속한 후 시도하세요.")

# 알림
def info(message):
    msgbox.showinfo("알림", message)

# 티킨터 세팅
root = Tk()
root.geometry("310x570")
root.title(f"미친메신저의정석 GUI v{displayVersion}")

# 프로그램 내 타이틀
title = Label(root, text=f"집가고싶다 Inc.\n미친메신저의정석 GUI v{displayVersion}", justify=LEFT)
title.grid(row=0, column=0, sticky=W)

# 연결 탭
connectFrame = LabelFrame(root, text="서버 접속", relief="solid", bd=1) # 연결 탭 프레임
putAdrLabel = Label(connectFrame, text="서버 주소 :") # 서버 주소 입력 라벨
serverAdrEntry = Entry(connectFrame) # 서버 주소 입력창
putPortLabel = Label(connectFrame, text="서버 포트 :") # 서버 포트 입력 라벨
serverPortEntry = Entry(connectFrame) # 서버 포트 입력창
putClientName = Label(connectFrame, text="이름 :") # 클라이언트이름 입력 라벨
clientNameEntry = Entry(connectFrame) # 클라이언트 입력창 (프로그램 내에서는 이름이라고만 표기)
helpButton = Button(connectFrame, text="도움", command=connectHelp) # 도움 버튼
connectButton = Button(connectFrame, text="서버 접속", command=connect) # 서버 접속 버튼

connectFrame.grid(row=1, column=0, columnspan=2, sticky=E+W)
putAdrLabel.grid(row=0, column=0, sticky=E)
serverAdrEntry.grid(row=0, column=1)
putPortLabel.grid(row=1, column=0, sticky=E)
serverPortEntry.grid(row=1, column=1)
putClientName.grid(row=2, column=0, sticky=E)
clientNameEntry.grid(row=2, column=1)
helpButton.grid(row=3, column=0, sticky=W)
connectButton.grid(row=3, column=1, sticky=E)

# 메시지 출력창
messageOutListbox = Listbox(root, selectmode="extended", width=27, height=20) # 입력창
messageScrollbar = Scrollbar(root, orient="vertical", command=messageOutListbox.yview) # 스크롤바
messageOutListbox.config(yscrollcommand=messageScrollbar.set)

messageOutListbox.grid(row=2, column=0, columnspan=2, sticky=W)
messageScrollbar.grid(row=2, column=1, sticky=N+E+S)

# 메시지 전송
messageInputEntry = Entry(root) # 메시지 입력창
messageInputEntry.bind("<Return>", send) # 입력창에서 엔터를 누르면 자동 전송
messageSendButton = Button(root, text="전송", command=send) # 메시지 전송 버튼

messageInputEntry.grid(row=3, column=0, sticky=E+W)
messageSendButton.grid(row=3, column=1, sticky=W)

# 접속 해제
disconnectButton = Button(root, text="접속 해제", command=disconnect)
disconnectButton.grid(row=4, column=0, sticky=W)

# 알림 기능
ringVar = IntVar()
ringChkbtn = Checkbutton(root, text="메시지 알림", variable=ringVar)
ringChkbtn.grid(row=4, column=0, columnspan=2)

root.mainloop()
