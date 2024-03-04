import tkinter as tk
import socket
from threading import Thread


def on_quit(e=None):
    input_message.set("/bye")
    send()


def send(e=None):
    message = input_message.get()
    sock.send(message.encode())
    input_message.set("")

    if message == "/bye":
        sock.close()
        window.quit()


def recv_message():
    while True:
        try:
            message = sock.recv(1024)
            chat_list.insert(tk.END, message.decode())
        except Exception:
            pass


IP = input("접속할 ip를 입력하세요: ")
PORT = 8080
if not IP:
    IP = "localhost"

print("{}:{}에 접속".format(IP, PORT))


# TKinter 화면 구성
window = tk.Tk()
window.title("Chatting Program")
window.protocol("WM_DELETE_WINDOW", on_quit)
mainframe = tk.Frame(window)
mainframe.pack(fill=tk.BOTH)
entryframe = tk.Frame(window)
entryframe.pack(side=tk.BOTTOM, fill=tk.BOTH)


scroll = tk.Scrollbar(mainframe)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
chat_list = tk.Listbox(mainframe, height=15, width=50, yscrollcommand=scroll.set)
chat_list.pack(side=tk.LEFT, fill=tk.BOTH)

input_message = tk.StringVar(value="")
input_box = tk.Entry(entryframe, textvariable=input_message)
input_box.bind("<Return>", send)
input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)

send_btn = tk.Button(entryframe, text="전송", command=send)
send_btn.pack(side=tk.RIGHT, fill=tk.X, padx=5, pady=5)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))


recv_thread = Thread(target=recv_message, daemon=True)
recv_thread.start()

window.mainloop()
