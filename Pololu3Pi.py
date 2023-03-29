# import libraries
import socket
import tkinter.messagebox
from tkinter import *
import time


# Making tkinter window class
class App:
    def __init__(self, master):
        # configure window
        # Zielony Led
        self.greenLedState = IntVar()
        self.greenLed = Checkbutton(master, text="Green Led", variable=self.greenLedState, justify="left", padx=20, pady=20)
        self.greenLed.place(x=0, y=0)
        # Czerwony Led
        self.redLedState = IntVar()
        self.redLed = Checkbutton(master, text="Red Led", variable=self.redLedState, justify="left", padx=20, pady=20)
        self.redLed.place(x=0, y=40)
        # Wprowadzenie ip
        self.ipFrame = Frame(master, width=100, height=50, bg="grey")
        self.ipFrame.place(x=120, y=0)
        # opis pola
        self.ipLabel = Label(self.ipFrame, text='Insert IP and connect')
        self.ipLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
        # Przycisk do ustalenia polaczenia
        self.connectionButton = Button(self.ipFrame, text="Connect", padx=40, pady=20, command=self.ConnectionButton)
        self.connectionButton.grid(column=1, row=1, padx=5, pady=5)
        # Pole do wprowadzenia koncowki ip
        self.ipEntry = Entry(self.ipFrame, width=3)
        self.ipEntry.grid(column=0, row=1, padx=5, pady=5)

    # Connect button
    def ConnectionButton(self):
        try:
            koncowkaIp = int(self.ipEntry.get())
        except ValueError:
            koncowkaIp = None

        if koncowkaIp is None or not (30 < koncowkaIp < 40):
            tkinter.messagebox.showinfo("Connection Status", "Wrong ip!")
        else:
            # ipRobota = "192.168.2." + str(koncowkaIp)
            # For now Im gonna use local ip for testing
            ipRobota = "127.0.0.1"
            port = 8000
            # print(ipRobota)
            my_socket.connect((ipRobota, port))
            # start data transmission
            self.DataTransmission()

    # Data transmission
    def DataTransmission(self):
        robotControlData = b"[010000]"
        my_socket.send(robotControlData)
        time.sleep(1)
        self.recvdata = my_socket.recv(1024).decode()
        print(self.recvdata)
        self.ipFrame.after(1000, self.DataTransmission)


if __name__ == "__main__":
    # Create a Socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Making window root
    root = Tk()
    root.title('Pololu3Pi')
    root.geometry('800x500')
    # calling gui
    app = App(root)
    root.mainloop()
