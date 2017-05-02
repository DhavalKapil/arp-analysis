from scapy.all import *

ARP_REQUEST = ARP.who_has
ARP_REPLY = ARP.is_at

def create_arp_packet(src_mac,
                      src_ip,
                      dest_mac,
                      dest_ip,
                      arp_type):
    # Creating ethernet packet structure
    ether = Ether()
    ether.dst = dest_mac
    ether.src = "a4:5d:36:6b:62:31"
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

def send_arp_packet(packet):
    sendp(packet)

def sniff_arp_packets(callback,
                      timeout):
    sniff(prn=callback,
          timeout=timeout,
          filter="arp",
          store=0)
