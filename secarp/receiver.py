import netifaces
import sys
import thread
from scapy.all import *

from lib import arp

def usage():
    print "Usage:"
    print "%s [interface] [dest_ip] [ARP_REPLY_WAIT_TIME(millis)]" \
        % (sys.argv[0])

def main():
    if len(sys.argv) != 4:
        usage()
        sys.exit()

    interface = sys.argv[1]
    dest_ip = sys.argv[2]
    arp_reply_wait_time = int(sys.argv[3])

    addresses = netifaces.ifaddresses(interface)
    src_mac = addresses[netifaces.AF_LINK][0]['addr']
    src_ip = addresses[netifaces.AF_INET][0]['addr']

    ip_mac_count = {}

    def packet_handler(packet):
        if packet[ARP].op == arp.ARP_REPLY and \
           packet[ARP].psrc == dest_ip:
            if packet[ARP].hwsrc in ip_mac_count:
                ip_mac_count[packet[ARP].hwsrc] += 1
            else:
                ip_mac_count[packet[ARP].hwsrc] = 1

    packet = arp.create_arp_packet(src_mac,
                                   src_ip,
                                   "FF:FF:FF:FF:FF:FF",
                                   dest_ip,
                                   arp.ARP_REQUEST)
    arp.send_arp_packet(packet)

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=arp_reply_wait_time/1000)

    print "Packets received:"
    for mac in ip_mac_count:
        print "Mac Address: %s, count = %d" % (mac, ip_mac_count[mac])

if __name__ == "__main__":
    main()
