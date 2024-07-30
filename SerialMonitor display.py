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
    comButton = Button(fenetre, text=onePort, font=('Calibri', '13'), 
                       height=1, width=50, 
                       command = functools.partial(initComPort, index = ports.index(onePort)))
    comButton.grid(row=ports.index(onePort), column=0)
    
dataCanvas = Canvas(data_fenetre, width=1200, height=900, bg='white')

dataCanvas.grid(row=0, column=1, rowspan=100)

vsb = Scrollbar(data_fenetre, orient='vertical', command=dataCanvas.yview)
vsb.grid(row=0, column=2, rowspan=100, sticky='ns')

dataCanvas.config(yscrollcommand = vsb.set)

dataFrame = Frame(dataCanvas, bg="white")
dataCanvas.create_window((10,0),window=dataFrame,anchor='nw')

def checkSerialPort():
    debut_chrono_dans_packet=5
    debut_type_msg=2
    num_puce=3
    if serialObj.isOpen() and serialObj.in_waiting:
        #pré-traitement du message 
        dernier_packet = str(serialObj.readline())
        print("avant traitement", dernier_packet)
        dernier_packet = dernier_packet[2 : -5 or None]
        #decode_msg(packet_a_decoder=dernier_packet, debut_chrono=debut_chrono_dans_packet, 
        #          dataFrame=dataFrame, num_puce=num_puce, debut_type_msg=debut_type_msg)
        print("apres traitement", dernier_packet)
        return dernier_packet
        

def decode_msg(packet_a_decoder, debut_chrono, dataFrame, debut_type_msg, num_puce):
    dernier_chrono = []
    dernier_chrono.clear()
    print(packet_a_decoder)
    # si message de type puce numero...
    if packet_a_decoder[debut_type_msg] == "P":

        # si puce numero 1 (hugo)
        if packet_a_decoder[num_puce] == '1':
            Label(dataFrame, text="Hugo : ").pack()

            # si caractere 'c' : debut du dernier chrono
            if (packet_a_decoder[debut_chrono-1] == 'C'):
                i = debut_chrono

                # parcourt le tableau depuis le chrono et s'arrete a la 1ere accolade
                while (packet_a_decoder[i] != "}" and packet_a_decoder[i] != ' '):
                    dernier_chrono.append(packet_a_decoder[i])
                    i += 1

                # conversion du tab dernier_chrono en int
                s = [str(integer) for integer in dernier_chrono]
                dernier_chrono = "".join(s)
                chronos_Hugo.append(int(dernier_chrono))
                Label(dataFrame, text=chronos_Hugo[len(chronos_Hugo)-1]).pack()

        #si puce numero 2 (maxime)
        elif packet_a_decoder[num_puce] == '2':
            Label(dataFrame, text="Maxime : ").pack()
            if (packet_a_decoder[debut_chrono-1] == 'C'):
                i = debut_chrono
                while (packet_a_decoder[i] != "}" and packet_a_decoder[i] != ' '):
                    #ajout du caractere au tableau 'dernier_chrono'
                    dernier_chrono.append(packet_a_decoder[i])
                    i += 1

                # conversion du tab dernier_chrono en int
                s = [str(integer) for integer in dernier_chrono]
                dernier_chrono = "".join(s)
                chronos_max.append(int(dernier_chrono))
                Label(dataFrame, text=chronos_max[len(chronos_max)-1]).pack()
    
def get_num(rawdata):
    num = ""
    while(len(rawdata) != 0 and rawdata[0] != ' '):
        num += rawdata[0]
        rawdata = rawdata[1:]

    return int(num), rawdata

def decode_msgV2(rawdata):
    if rawdata[0] == '{' and rawdata[-1] == '}':
        rawdata = rawdata[1:-1]

        puceId = 0
        lapTime = 0
        temp = 0
        battery = 0

        while len(rawdata) != 0:
            if (rawdata[0] == ' '):
                rawdata = rawdata[1:]
            elif (rawdata[0] == 'P'):
                rawdata = rawdata[1:]
                puceId, rawdata = get_num(rawdata)
            elif (rawdata[0] == 'C'):
                rawdata = rawdata[1:]
                lapTime, rawdata = get_num(rawdata)
            elif (rawdata[0] == 'T'):
                rawdata = rawdata[1:]
                temp, rawdata = get_num(rawdata)
            elif (rawdata[0] == 'B'):
                rawdata = rawdata[1:]
                battery, rawdata = get_num(rawdata)

        return {"puceid" : puceId, "laptime" : lapTime, "temp": temp, "battery" :  battery}
    else:
        return None


def affichage():
    print("bite")

while True:
    fenetre.update()
    checkSerialPort()
    decode_msgV2(rawdata=str(checkSerialPort()))
    
    dataCanvas.config(scrollregion=dataCanvas.bbox("all"))
    
    
    
    

