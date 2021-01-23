from scapy.all import *
import colorama
from colorama import Fore
import threading
import time
# autoreset.. not to need end of color
colorama.init(autoreset=True)
ip = input("Enter IP address: ")
portRange = input("Enter port range (X-Y): ")
thNumber = int(input("Enter the number of threads to use: "))
portStatusList = []
x = []  # threads
IPstatus = int()


def checkhost():
    global IPstatus
    ping = IP(dst=ip)/ICMP()
    res = sr1(ping, timeout=1, verbose=0)
    if res == None:
        print(Fore.RED + "The host is down")
        IPstatus = 0
    else:
        print(Fore.GREEN + "The host is up")
        IPstatus = 1


def checkport():
    portList = portRange.split("-")
    try:
        Xrange = int(portList[0])
        Yrange = int(portList[1])
    except:
        print("Use the correct sintaxis (e.g. 0-8080)")
    equalPart = int((Yrange - Xrange) / thNumber)
    for i in range(0, thNumber):
        x.append(threading.Thread(target=checkPORTthread, args=(
            equalPart * i + 1, equalPart * (i + 1), i)))
    for i in range(0, thNumber):
        x[i].start()
        time.sleep(0.1)


def checkPORTthread(Xrange, Yrange, threadNumber):
    print("Thread " + str(threadNumber) +
          " WORKING! for range " + str(Xrange) + "-" + str(Yrange))
    for port in range(Xrange, Yrange + 1):
        tcpRequest = IP(dst=ip)/TCP(dport=port, flags="S")
        tcpResponse = sr1(tcpRequest, timeout=0.4, verbose=0)
        try:
            if tcpResponse.getlayer(TCP).flags == "SA":
                print(Fore.GREEN + str(port) + " is open")
                portStatusList.append(Fore.GREEN + str(port) + " is open")
            else:
                pass
                # print(Fore.RED + str(port) + " is closed")
        except AttributeError:
            pass
            #print(Fore.RED + str(port) + " NO está a la escucha")


def __main__():
    global IPstatus
    checkhost()
    start = time.time()
    if IPstatus == 1:
        checkport()
        for i in range(0, thNumber):
            x[i].join()
        print("\n\nSummary: ")
        if IPstatus == 1:
            print(Fore.GREEN + "The host is up")
        else:
            print(Fore.RED + "The host is down")
        print('\n'.join(portStatusList))
    end = time.time()
    print("The port scan took: " + str(int(end - start)) + "s")


__main__()
