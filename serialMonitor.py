import serial
import sys
import _thread
from tkinter import *


class ArduinoCommunicator():
    def __init__(self, port, baud = 115200):
        self.ser = serial.Serial(port, baud)

    def read(self):
        return self.ser.readline().decode('utf-8')

    def isAvailable(self):
        return self.ser.isOpen()

    def write(self, data):
        return self.ser.write(data.encode('utf-8'))

    def close(self):
        self.ser.close()


class SerialMonitorGui:
    serialComs = 0
    def __init__(self,master):
        self.root = master
        self.createGui()
        self.isConnected = False;
        _thread.start_new_thread(self.handleCommunication, ())
        self.root.bind("<Return>",self.handleSend)

    def createGui(self):
        self.writingFrame = Frame(self.root)
        self.monitorFrame = Frame(self.root)
        self.connectionFrame = Frame(self.root)
        self.writingFrame.pack(fill=BOTH, side = TOP)
        self.writingFrame.columnconfigure(0,weight=1)
        self.toSendLabel = Button(self.writingFrame,text="Send:", command = self.handleSend)
        self.toSendLabel.grid(row=0,column=0,sticky=E+W)
        self.writingFrame.columnconfigure(1,weight=9)
        self.textEntry = Entry(self.writingFrame)
        self.textEntry.grid(row=0,column=1,sticky=E+W)
        self.monitorFrame.pack(expand=True, fill=BOTH)
        self.monitorFrame.columnconfigure(0,weight=9)
        self.monitorFrame.columnconfigure(1,weight=1)
        self.monitorFrame.rowconfigure(0,weight=10)
        self.scrollbar = Scrollbar(self.monitorFrame)
        self.scrollbar.grid(row = 0, column=1, sticky=N+S+W)
        self.listbox = Listbox(self.monitorFrame)
        self.listbox.grid(row = 0, column = 0,sticky=N+S+E+W)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.connectionFrame.pack(side=BOTTOM)
        self.portVar = StringVar(self.root)
        self.baudVar = StringVar(self.root)
        self.portOptions = ["/dev/ttyACM0",'/dev/ttyACM1']
        self.baudOptions = ['9600','115200']
        self.portVar.set(self.portOptions[0])
        self.baudVar.set(self.baudOptions[0])
        self.portMenu = OptionMenu(self.connectionFrame,self.portVar, *self.portOptions)
        self.baudMenu = OptionMenu(self.connectionFrame,self.baudVar, *self.baudOptions)
        self.portLabel = Label(self.connectionFrame, text="Port:").grid(row = 3, column = 1)
        self.portMenu.grid(row = 3, column = 2)
        self.baudLabel = Label(self.connectionFrame, text="Baud:").grid(row = 3, column = 3)
        self.baudMenu.grid(row = 3, column = 4)
        self.openButton = Button(self.connectionFrame, text="Open", command=self.openComs)
        self.openButton.grid(row = 3, column = 5)


    def handleSend(self,event):
        if(self.isConnected == True):
            self.serialComs.write(self.textEntry.get() + "\n")
            self.listbox.insert(END,self.textEntry.get())
            self.textEntry.delete(0,END)

    def openComs(self):
        attempts = 1
        success = False
        try:
            print("Attempting to open" + self.portVar.get())
            self.serialComs = ArduinoCommunicator(self.portVar.get())

        except Exception as e:
            print(e)
            #make a popup?
            print("Failed to open")
            return
        self.isConnected = True

    def handleCommunication(self):
        while True:
            while(self.isConnected == False):
                #do nothing....
                pass
            try:
                while(self.isConnected == True):
                    print("Scanning")
                    if(self.serialComs.isAvailable() == True):
                        message = self.serialComs.read()
                        print(message)
                        self.listbox.insert(END,message)
            except serial.serialutil.SerialException:
                print("Communication error, trying again!")
                serialComs = ArduinoCommunicator(self.portVar.get())


def main():
    #three different frames
    root = Tk()
    gui = SerialMonitorGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
