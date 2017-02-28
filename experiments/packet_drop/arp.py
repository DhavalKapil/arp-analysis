from scapy.all import *

ARP_REQUEST = ARP.who_has
ARP_REPLY = ARP.is_at

def create_arp_packet(interface,
                      src_mac,
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
    # Presently only for ethx interface (TODO)
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
