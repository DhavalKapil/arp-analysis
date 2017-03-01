import sys
from scapy.all import *

from lib import arp

def usage():
    print "Usage:"
    print "%s [server_ip] [client_ip] [time(seconds)]" % (sys.argv[0])

def main():
    if len(sys.argv) != 4:
        usage()
        sys.exit()

    server_ip = sys.argv[1]
    client_ip = sys.argv[2]
    seconds = int(sys.argv[3])

    request_packets = []
    reply_packets = []

    def packet_handler(packet):
        if packet[ARP].op == arp.ARP_REQUEST and \
           packet[ARP].psrc == client_ip and \
           packet[ARP].pdst == server_ip:
            request_packets.append(packet)
        elif packet[ARP].op == arp.ARP_REPLY and \
             packet[ARP].psrc == server_ip and \
             packet[ARP].pdst == client_ip:
            reply_packets.append(packet)

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=seconds)

    print "%d request packets logged" % len(request_packets)
    print "%d reply packets logged" % len(reply_packets)

if __name__ == '__main__':
    main()
