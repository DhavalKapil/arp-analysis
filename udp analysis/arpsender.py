from scapy.all import *
import netifaces
import sys

def create_arp_packet(src_mac,
                      src_ip,
                      dest_mac,
                      dest_ip,
                      arp_type):
    # Creating ethernet packet structure
    ether = Ether()
    ether.dst = dest_mac
    ether.src = src_mac
    ether.type = 0x806 # ARP protocol

    # Creating arp packet structure
    arp = ARP()
    arp.hwtype = 1
    arp.ptype = 0x800 # IP protocol
    arp.hwlen = 6
    arp.plen = 4
    arp.op = arp_type
    arp.hwsrc = src_mac
    arp.psrc = src_ip
    arp.hwdst = dest_mac
    arp.pdst = dest_ip

    return ether/arp

interface = sys.argv[1]
dest_mac = sys.argv[2]
dest_ip = sys.argv[3]
packetCount = int(sys.argv[4])

addresses = netifaces.ifaddresses(interface)
src_mac = addresses[netifaces.AF_LINK][0]['addr']
src_ip = addresses[netifaces.AF_INET][0]['addr']

i = 0
while i<packetCount:
	packet = create_arp_packet(src_mac,
                               src_ip,
                               dest_mac,
                               dest_ip,
                               ARP.who_has) 
	sendp(packet)
	i+=1
