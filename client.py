import time
import paramiko
import colorama
import subprocess
from colorama import Fore,Style,Back
HOST='192.168.1.36'
USER='pi'
PASS='pi'
YELLOW = "\x1b[1;33;40m"
RED = "\x1b[1;31;40m"

def mostrar_menu():
    print('''
    1)lanzar escaneo de red
    2)arp spoofing
    3)DHCP spoofing
    4)clonar pagina
    5)SHELL2
          '''
          )



def shell():
    subprocess.run(f" ssh -T  {USER}@{HOST} ", shell=True)




if __name__ == '__main__':
    colorama.init()
    cmd = input(Fore.RED + "raspberry" + "☠" + Fore.WHITE + "$")
    Fore.WHITE
    mostrar_menu()

    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(HOST,username='pi')
    stdin, stdout, stderr=client.exec_command('python project/prueba.py')
    time.sleep(1)
    result=stdout.read().decode()

    shell()

    print(result)