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
chronos_Hugo=[]

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
    dernier_chrono=[]
    dernier_chrono.clear()
    debut_chrono=5
    if serialObj.isOpen() and serialObj.in_waiting:
        #traitement du message 
        recentPacket = str(serialObj.readline())
        recentPacket = recentPacket[: -5 or None]
        recentPacket += "}"
        #Label(dataFrame, text=recentPacket, bg = "white").pack()
        
        if recentPacket[2] == "P": #si message de type puce numero...
            if recentPacket[3] == '1': #si puce numero 1 (hugo)
                Label(dataFrame, text="Hugo : ").pack() 
                if(recentPacket[debut_chrono-1] == 'C'): #si caractere 'c' : debut du dernier chrono
                    i=debut_chrono
                    while(recentPacket[i] != "}"): #parcourt le tableau depuis le chrono
                        dernier_chrono.append(recentPacket[i])
                        i+=1
                    #conversion du tab dernier_chrono en int 
                    s = [str(integer) for integer in dernier_chrono]
                    dernier_chrono = "".join(s)
                    #ajout du dernier chrono dans le tab chronos_hugo
                    chronos_Hugo.append(int(dernier_chrono))
                    Label(dataFrame, text=chronos_Hugo[len(chronos_Hugo)-1]).pack()

            elif recentPacket[3] == '2': #si puce numero 2 (maxime)
                Label(dataFrame, text="Maxime").pack()
                if(recentPacket[debut_chrono-1] == 'C'):
                    i=debut_chrono
                    while(recentPacket[i] != "}"):
                        dernier_chrono.append(recentPacket[i])
                        i+=1
                    #conversion du tab dernier_chrono en int
                    s = [str(integer) for integer in dernier_chrono]
                    dernier_chrono = "".join(s)
                    chronos_max.append(int(dernier_chrono))
                    Label(dataFrame, text=chronos_max[len(chronos_max)-1]).pack()

#def decode_msg(packet, chronos):
    
while True:
    fenetre.update()
    checkSerialPort()
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))
    
    
    

