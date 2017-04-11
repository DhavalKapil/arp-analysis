import netifaces
import sys
import json
import time
from scapy.all import *

from lib import arp

def usage():
    print "Usage:"
    print "%s [time(seconds)]" % (sys.argv[0])

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit()

    seconds = int(sys.argv[1])

    packet_log = []
    def packet_handler(packet):
        print(packet)
        packet_log.append({
            "timestamp": int(time.time()),
            "packet": {
                "eth_header": {
                    "dst": packet[Ether].dst,
                    "src": packet[Ether].src,
                    },
                "arp_header": {
                    "type": "request" if packet[ARP].op == arp.ARP_REQUEST else "reply",
                    "source_mac": packet[ARP].hwsrc,
                    "source_ip": packet[ARP].psrc,
                    "dest_mac": packet[ARP].hwdst,
                    "dest_ip": packet[ARP].pdst
                    }
                }
            })

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=seconds)

    with open("log.json", "w") as outfile:
        json.dump(packet_log, outfile)

    print "Finished successfully"

if __name__== "__main__":
    main()
