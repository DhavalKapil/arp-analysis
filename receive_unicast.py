import netifaces
import sys

from scapy.all import *

from lib import arp

def usage():
    print "Usage:"
    print "%s [interface] [new_mac] [time(seconds)]" % (sys.argv[0])

def main():
    if len(sys.argv) != 4:
        usage()
        sys.exit()

    interface = sys.argv[1]
    new_mac = sys.argv[2]
    seconds = int(sys.argv[3])

    addresses = netifaces.ifaddresses(interface)
    src_ip = addresses[netifaces.AF_INET][0]['addr']

    def packet_handler(packet):
        if packet[ARP].pdst == src_ip and \
           packet[ARP].op == arp.ARP_REQUEST:
            reply_packet = arp.create_arp_packet(new_mac,
                                                 src_ip,
                                                 packet[ARP].hwsrc,
                                                 packet[ARP].psrc,
                                                 arp.ARP_REPLY)
            arp.send_arp_packet(reply_packet)

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=seconds)

if __name__ == '__main__':
    main()
