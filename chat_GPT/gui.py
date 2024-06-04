from pathlib import Path
from tkinter import *
from chatGPT_caller import chatGPT
import socket

class GUI:
    def __init__(self, server=""):
        self.chat_gpt=chatGPT()
        window = Tk()
        window.geometry("640x480")
        window.configure(bg = "#FFFFFF")

        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 480,
            width = 640,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_text(
            100.0,
            32.0,
            anchor="nw",
            text="Assign tasks to machines here:",
            fill="#000000",
            font=("清松手寫體1-Medium", 30 * -1, 'bold')
        )
        ""
        canvas.create_text(
            277.0,
            218.0,
            anchor="nw",
            text="console log",
            fill="#838383",
            font=("清松手寫體1-Medium", 16 * -1)
        )


        button_1 = Button(
            borderwidth=0,
            highlightthickness=0,
            text="Send",
            font=("清松手寫體1-Medium", 24 * -1),
            command=self.send,
            relief="flat"
        )
        button_1.place(
            x=287.0,
            y=172.0,
            width=67.0,
            height=32.0
        )

        entry_image_1 = PhotoImage(
            file="./assets/frame0/entry_1.png")
        entry_bg_1 = canvas.create_image(
            321.0,
            115.0,
            image=entry_image_1
        )
        self.entry_1 = Text(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("清松手寫體1-Medium", 16 * -1),
            highlightthickness=0
        )
        self.entry_1.insert(END, "Please grab the red block and then grab the blue block.") 
        self.entry_1.place(
            x=66.0,
            y=78.0,
            width=510.0,
            height=72.0
        )

        entry_image_2 = PhotoImage(
            file="./assets/frame0/entry_2.png")
        entry_bg_2 = canvas.create_image(
            320.0,
            353.5,
            image=entry_image_2
        )

        self.entry_2 = Listbox(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("清松手寫體1-Medium", 12 * -1),
            highlightthickness=0
        )
        self.entry_2.insert(END, "")
        self.entry_2.place(
            x=172.0,
            y=245.0,
            width=296.0,
            height=220.0
        )
        self.server=server
        self.response=""
        window.resizable(False, False)
        window.mainloop()
    def send(self):
        text=self.entry_1.get("1.0", END)
        self.Log("Send to chatGPT: "+text)
        self.Log("Waiting for response...")
        self.response=self.chat_gpt.ask(text)
        self.Log("chatGPT responsed: "+self.response)
        self.send2server()
    def Log(self, newLog):
        self.entry_2.insert(0, newLog)
        self.entry_2.update()

    def send2server(self):
        self.server.sendall(self.response.encode())
        Executing = self.server.recv(1024).decode()

        if Executing=="Executing":
            self.Log("Executing")
            Exe_end = self.server.recv(1024).decode()
            self.Log("Execution ends")

    #def send2client(self, idx):

if __name__=="__main__":
    gui=GUI()