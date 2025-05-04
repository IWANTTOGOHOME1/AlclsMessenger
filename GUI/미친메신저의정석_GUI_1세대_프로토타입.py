#집가고싶다 Inc.
#미친메신저의정석 GUI 1세대

#미친메신저의정석 GUI 1세대 v1.0.0
#AMG100

#패키지
from tkinter import * # G U I !!!!
import socket
import threading

#개발 버전 변수
version = "AMGP"
displayVersion = "1.0.0"

#건드리면 안되는 변수
outputLog = ""
globalSocket = ""

#서버 접속 함수
def connect():
    global name
    global globalSocket
    try:
        HOST = ipInput.get()
        name = nameInput.get()
    except Exception as e:
        output(f"오류가 발생했습니다.\n{e}")
        return
    try:
        PORT = int(portInput.get())
    except:
        output("포트를 정수형 값으로 입력하세요!")
        return
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((HOST, PORT))
        communicating = threading.Thread(target=communicate, args=(clientSocket, ))
        communicating.start()
        globalSocket = clientSocket
    except Exception as e:
        output(f"서버에 접속할수 없습니다.\n{e}")

def communicate(clientSocket):
    while True:
        rcvdMsg = clientSocket.recv(1024).decode()
        if rcvdMsg == "name?": #서버가 이름 정보 물어보면?
            clientSocket.sendall(name.encode())
        elif rcvdMsg == "info?": #서버가 버전 정보 물어보면?
            clientSocket.sendall(version.encode())
        else:
            if not rcvdMsg: #서버가 닫히면
                output("\n\n서버가 닫혔거나 네트워크에 문제가 있는 것 같습니다.")
            output(rcvdMsg)

def output(log):
    outputLabel.insert(END, log)
    outputLabel.grid(row=0, column=2)
    outputLabel.see(END)

def send():
    globalSocket.sendall(messageText.get().encode())
    messageText.insert(0, "")
    messageText.grid(row=6, column=2)

def clear():
    outputLabel.delete(0, END)
    outputLabel.grid(row=0, column=2)

#티킨터 기본세팅
root = Tk()
root.title("미친메신저의정석 GUI 1세대 프로토타입")
root.geometry("780x240")
root.resizable(True, True)

#상표(?)
welcome = Label(root, text="집가고싶다 Inc.\n미친메신저의정석 GUI 1세대 프로토타입")
welcome.grid(row=0, column=0)
# welcome.pack()

connectFrame = LabelFrame(root, relief="solid", bd=1, text="서버")
connectFrame.grid(row=1, column=0)

#서버주소 입력칸
ipInput = Entry(connectFrame)
# ipInput.insert(0, "messenger.iwanttogohome.net")
ipInput.insert(0, "접속할 서버의 주소를 입력하세요.")
ipInput.pack()
# ipInput.grid(row=1, column=0)

#서버포트 입력칸
portInput = Entry(connectFrame)
# portInput.insert(0, "887")
portInput.insert(0, "접속할 서버의 포트를 입력하세요.")
portInput.pack()
# portInput.grid(row=2, column=0)

nameInput = Entry(connectFrame)
nameInput.insert(0, "이 클라이언트의 이름을 입력하세요.")
nameInput.pack()
# nameInput.grid(row=3, column=0)

#접속버튼
connectButton = Button(connectFrame, text="접속", command=connect)
connectButton.pack(side=RIGHT)
# connectButton.grid(row=4, column=0)

#메시지 입력
messageText = Entry(root, width=50)
# messageText.pack()
messageText.grid(row=6, column=2)

#메시지 전송
sendButton = Button(root, text="전송", command=send)
# sendButton.pack()
sendButton.grid(row=6, column=3)

# clearButton = Button(root, text="초기화", command=clear)
# # clearButton.pack()
# clearButton.grid(row=0, column=5)

outputLabel = Listbox(root, width=50)
logscrollbar = Scrollbar(root, orient="vertical", command=outputLabel.yview)
# outputLabel.pack()

outputLabel.config(selectmode="extended", height=10, yscrollcommand=logscrollbar.set)

outputLabel.grid(row=0, column=2, rowspan=5)
logscrollbar.grid(row=0, column=3, rowspan=5, sticky=N+W+S)

root.mainloop()
