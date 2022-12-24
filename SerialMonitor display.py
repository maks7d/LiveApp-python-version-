from tkinter import *
import serial.tools.list_ports
import functools

ports = serial.tools.list_ports.comports()
serialObj = serial.Serial()

fenetre = Tk()
data_fenetre = Tk()
fenetre.config(bg='grey')
menu = Menu(fenetre)
Ports = Menu(menu)
Ports.add_command(label="")
menu.add_cascade(label="Ports", menu=Ports)

fenetre.config(menu=menu)

chronos_max = []

def initComPort(index):
    currentPort = str(ports[index])
    comPortVar = str(currentPort.split(' ')[0])
    print(comPortVar)
    serialObj.port = comPortVar
    serialObj.baudrate = 9600
    serialObj.open()

for onePort in ports:
    comButton = Button(fenetre, text=onePort, font=('Calibri', '13'), height=1, width=50, command = functools.partial(initComPort, index = ports.index(onePort)))
    comButton.grid(row=ports.index(onePort), column=0)

dataCanvas = Canvas(data_fenetre, width=1200, height=900, bg='white')
dataCanvas.grid(row=0, column=1, rowspan=100)

vsb = Scrollbar(data_fenetre, orient='vertical', command=dataCanvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')

dataCanvas.config(yscrollcommand = vsb.set)

dataFrame = Frame(dataCanvas, bg="white")
dataCanvas.create_window((10,0),window=dataFrame,anchor='nw')


def checkSerialPort():
    if serialObj.isOpen() and serialObj.in_waiting:
        recentPacket = serialObj.readline()
        recentPacketString = recentPacket.decode('utf').rstrip('\n')
        Label(dataFrame, text=recentPacketString, bg = "white").pack()
        return recentPacketString

def decode_chronos():
    #gestion chrono recu
    if(dernier_packet_reçu == "chronos"):
        print("chronos")


while True:
    fenetre.update()
    checkSerialPort()
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))
    dernier_packet_reçu = str(checkSerialPort())
    decode_chronos()
    

