import time
import paramiko
import colorama
import subprocess
import requests
from colorama import Fore,Style,Back





HOST='192.168.1.100'
USER='pi'
YELLOW = "\x1b[1;33;40m"
RED = "\x1b[1;31;40m"
hosts=list()
macs=list()

def mostrar_menu():
    print('''
    1)lanzar escaneo de red
    2)arp spoofing
    3)DHCP spoofing
    4)clonar pagina
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

    (stdin, stdout, stderr) = client.exec_command("sudo python")

    pass

def shell():
    subprocess.run(f" ssh -T  {USER}@{HOST} ", shell=True)

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
    stdin, stdout, stderr=client.exec_command("route | grep default | awk '{print $2}'")
    gw=stdout.read().decode()
    return gw








def spoof(victima):

    print(get_gateway())



if __name__ == '__main__':
    colorama.init()


######  CONEXION POR SSH Y ESCANEO YA PARSEADO
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST,username='pi')
    stdin, stdout, stderr=client.exec_command('sudo python3 project/enumerate.py')#se realiza un escaneo nada mas comenzar
    parsear_escaneo(stdout.read().decode())


    while 1:
        mostrar_menu()
        cmd = input(Fore.RED + "raspberry" + Fore.WHITE + "$")
        Fore.WHITE
        if cmd=='1':
            mostrar_escaneo(0)
        if cmd=="2":
            mostrar_escaneo(0)
            victima = input("SELECCIONA VICTIMA  $")
            spoof(int(victima))





