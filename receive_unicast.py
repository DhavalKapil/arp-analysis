import netifaces
import sys

from scapy.all import *

from lib import arp

def usage():
    print "Usage:"
    print "%s [interface] [new_mac] [new_ip] [time(seconds)]" % (sys.argv[0])

def main():
    if len(sys.argv) != 5:
        usage()
        sys.exit()

    interface = sys.argv[1]
    new_mac = sys.argv[2]
    new_ip = sys.argv[3]
    seconds = int(sys.argv[4])

    def packet_handler(packet):
        if packet[ARP].pdst == new_ip and \
           packet[ARP].op == arp.ARP_REQUEST:
            reply_packet = arp.create_arp_packet(new_mac,
                                                 new_ip,
                                                 packet[ARP].hwsrc,
                                                 packet[ARP].psrc,
                                                 arp.ARP_REPLY)
            arp.send_arp_packet(reply_packet)

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=seconds)

if __name__ == '__main__':
    main()
