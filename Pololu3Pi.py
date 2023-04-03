# import libraries
import socket
import tkinter.messagebox
from tkinter import *
import time


# Making tkinter window class
class App:
    def __init__(self, master):
        # configure window
        self.ledFrame = Frame(master)
        self.ledFrame.place(x=0, y=0)
        # Zielony Led
        self.greenLedState = IntVar()
        self.greenLed = Checkbutton(self.ledFrame, text="Green Led", variable=self.greenLedState)
        self.greenLed.pack(anchor='w', padx=20, pady=15)
        # Czerwony Led
        self.redLedState = IntVar()
        self.redLed = Checkbutton(self.ledFrame, text="Red Led", variable=self.redLedState)
        self.redLed.pack(anchor='w', padx=20, pady=14)
        # Wprowadzenie ip
        self.ipFrame = Frame(master)
        self.ipFrame.place(x=120, y=0)
        # opis pola
        self.ipLabel = Label(self.ipFrame, text='Insert IP and connect')
        self.ipLabel.grid(column=0, row=0, padx=15, pady=16, columnspan=2)
        # Przycisk do ustalenia polaczenia
        self.connectionButton = Button(self.ipFrame, text="Connect", command=self.ConnectionButton)
        self.connectionButton.grid(column=1, row=1, padx=5, pady=14)
        # Pole do wprowadzenia koncowki ip
        self.ipEntry = Entry(self.ipFrame, width=3)
        self.ipEntry.grid(column=0, row=1, padx=5, pady=14)
        # Sliders for motors
        # Drive forward 0 - 127
        # Drive backward 128 - 255
        # Sliders Frame
        self.slidersFrame = Frame(master)
        self.slidersFrame.place(x=55, y=105)
        # Slider for left motor control
        # intvalue for control
        self.leftMotorValue = IntVar()
        self.sliderLeftMotor = Scale(self.slidersFrame, from_=127, to=-127, variable=self.leftMotorValue)
        self.sliderLeftMotor.grid(column=0, row=0)
        # Slider for right motor control
        # intvalue for control
        self.rightMotorValue = IntVar()
        self.sliderRightMotor = Scale(self.slidersFrame, from_=127, to=-127, variable=self.rightMotorValue)
        self.sliderRightMotor.grid(column=1, row=0)
        # Button for stop motors (set value to 0)
        self.stopButton = Button(self.slidersFrame, text="Stop motors", width=20, bg="#A00000", activebackground="#FF0000", fg="#FFFF00", command=self.StopMotors)
        self.stopButton.grid(column=0, row=1, columnspan=2)
        # Creating table for visualize sensor data
        self.sensorFrame = Frame(master)
        self.sensorFrame.place(x=0, y=236)
        self.sensorLabel = Label(self.sensorFrame, text="Sensors Value:")
        self.sensorLabel.grid(row=0, column=0, columnspan=2)
        # Creating labels
        self.sensorListKeys = ['Status', 'Bateria', 'Czujnik #1', 'Czujnik #2', 'Czujnik #3', 'Czujnik #4', 'Czujnik #5']
        for r in range(7):
            for c in range(2):
                self.e = Entry(self.sensorFrame, width=21, justify="center", cursor="arrow")
                self.e.grid(row=r + 1, column=c)
                if (c % 2 != 0):
                    continue
                self.e.insert(END, self.sensorListKeys[r])
                self.e.configure(state="disabled", disabledforeground="black")
        # Ip init
        self.ipRobota = None
        # Create button for disconecting
        self.disconectButton = Button(self.sensorFrame, text="Disconect", width=20, bg="#A00000", activebackground="#FF0000", fg="#FFFF00", command=self.Disconect)
        self.disconectButton.grid(row=8, column=0, columnspan=2)

    # Disconect button
    def Disconect(self):
        if self.ipRobota is not None:
            self.my_socket.send(b"[000000]")
            recvData = self.my_socket.recv(1024).decode()
            self.DecodeSensorValues(recvData)
            self.UpdateTableData()
            self.my_socket.close()
            self.ipFrame.after_cancel(self.transsmissionLoop)
            self.ipRobota = None

    # Connect button
    def ConnectionButton(self):

        try:
            koncowkaIp = int(self.ipEntry.get())
        except ValueError:
            koncowkaIp = None

        if koncowkaIp is None or not (30 < koncowkaIp < 40):
            tkinter.messagebox.showinfo("Connection Status", "Wrong ip!")
        else:
            if self.ipRobota is not None:
                self.StopMotors()
                self.my_socket.send(b"[000000]")
                recvData = self.my_socket.recv(1024).decode()
                self.DecodeSensorValues(recvData)
                self.UpdateTableData()
                self.my_socket.close()
                self.ipFrame.after_cancel(self.transsmissionLoop)
            # ipRobota = "192.168.2." + str(koncowkaIp)
            # For now Im gonna use local ip for testing
            self.ipRobota = "127.0.0.1"
            port = 8000
            # print(ipRobota)
            # Create a Socket
            self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.my_socket.connect((self.ipRobota, port))
                # start data transmission
                self.DataTransmission()
            except ConnectionRefusedError:
                tkinter.messagebox.showinfo("Connection Status", "Connection refused!")

    # Data transmission
    def DataTransmission(self):
        robotControlData = self.DataCalc()
        self.my_socket.send(bytes(robotControlData.encode()))
        # print(robotControlData)
        time.sleep(1)
        recvData = self.my_socket.recv(1024).decode()
        # Now i need to decode sensor values
        self.DecodeSensorValues(recvData)
        self.UpdateTableData()
        print(recvData)
        self.transsmissionLoop = self.ipFrame.after(1000, self.DataTransmission)

    # Calculating data
    def DataCalc(self):
        # Retrieving data from gui
        greenLedState = self.greenLedState.get()
        redLedState = self.redLedState.get()
        leftMotor = self.leftMotorValue.get()
        rightMotor = self.rightMotorValue.get()
        # ---TEST---
        # print(greenLedState)
        # print(redLedState)
        # ----------
        # Setting bits associated with leds
        if greenLedState == 1 and redLedState == 1:
            dataLed = "[03"
        elif greenLedState == 1:
            dataLed = "[01"
        elif redLedState == 1:
            dataLed = "[02"
        else:
            dataLed = "[00"
        # Setting bits for left motor control
        if leftMotor >= 0:
            leftMotorData = leftMotor
        else:
            leftMotorData = 255 + leftMotor
        # print(hex(leftMotorData))
        # Setting bits for right motor control
        if rightMotor >= 0:
            rightMotorData = rightMotor
        else:
            rightMotorData = 255 + rightMotor
        # print(hex(rightMotorData))
        leftMotorData = hex(leftMotorData)[2:]
        rightMotorData = hex(rightMotorData)[2:]
        # checking len
        if len(leftMotorData) < 2:
            leftMotorData = "0" + leftMotorData
        if len(rightMotorData) < 2:
            rightMotorData = "0" + rightMotorData
        rightMotorData += "]"
        # print(leftMotorData)
        returnedData = dataLed + leftMotorData + rightMotorData
        return returnedData

    # stopping motors
    def StopMotors(self):
        self.sliderLeftMotor.set(0)
        self.sliderRightMotor.set(0)

    # Decode sensor values
    def DecodeSensorValues(self, recvData):
        self.sensorValues = list()
        # Status data
        statusData = int("0x" + recvData[1:3], base=16)
        # print(statusData)
        # Battery status
        batteryStatus = int("0x" + recvData[5:7] + recvData[3:5], base=16)
        # print(batteryStatus)
        # Sensor #1
        firstSensor = int("0x" + recvData[9:11] + recvData[7:9], base=16)
        # print("0x" + recvData[7:11])
        # Sensor #2
        secondSensor = int("0x" + recvData[13:15] + recvData[11:13], base=16)
        # print("0x" + recvData[11:15])
        # Sensor #3
        thirdSensor = int("0x" + recvData[17:19] + recvData[15:17], base=16)
        # print("0x" + recvData[15:19])
        # Sensor #4
        fourthSensor = int("0x" + recvData[21:23] + recvData[19:21], base=16)
        # print("0x" + recvData[19:23])
        # Sensor #5
        fifthSensor = int("0x" + recvData[25:27] + recvData[23:25], base=16)
        # print("0x" + recvData[23:27])
        self.sensorValues = [statusData, batteryStatus, firstSensor, secondSensor, thirdSensor, fourthSensor, fifthSensor]

    # Update data in table
    def UpdateTableData(self):
        for r in range(7):
            for c in range(2):
                self.e = Entry(self.sensorFrame, width=21, justify="center", cursor="arrow")
                self.e.grid(row=r + 1, column=c)
                if (c % 2 != 0):
                    self.e.delete(END)
                    self.e.insert(END, self.sensorValues[r])
                    continue
                self.e.delete(END)
                self.e.insert(END, self.sensorListKeys[r])
                self.e.configure(state="disabled", disabledforeground="black")


if __name__ == "__main__":
    # Making window root
    root = Tk()
    root.title('Pololu3Pi')
    root.geometry('255x420')
    root.configure(bg='#dddddd')
    # calling gui
    app = App(root)
    root.mainloop()
