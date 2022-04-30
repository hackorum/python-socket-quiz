import socket
from threading import Thread
from tkinter import *

# nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 5002

client.connect((ip_address, port))


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = Label(self.login, text="Please login to continue",
                         justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go = Button(self.login, text="CONTINUE", font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.window.mainloop()

    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title('QUIZ')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")

        self.labelHead = Label(self.window, bg="#17202A", fg="#eaecee",
                               text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.window, width=450, bg="#abb2b9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(self.window, width=20, height=2, bg="#17202a",
                             fg="#eaecee", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        self.textCons.config(cursor="arrow")

        self.labelBottom = Label(self.window, bg="#abb2b9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom, bg="#2c3e50",
                              fg="#eaecee", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06,
                            rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold",
                                width=20, bg="#abb2b9", command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008,
                             relheight=0.06, relwidth=0.22)

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = Thread(target=self.write)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode("utf-8")
                if message == "NICKNAME":
                    client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except:
                print("An error occured")
                client.close()
                break

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            break

    def show_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+'\n\n')
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)


g = GUI()


# def write():
#     while True:
#         message = "{}:{}".format(nickname, input(""))
#         client.send(message.encode("utf-8"))


# write_thread = Thread(target=write)
# write_thread.start()
