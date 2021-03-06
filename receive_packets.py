import netifaces
import sys
import time
from datetime import datetime
from scapy.all import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pp

from lib import arp

def usage():
    print "Usage:"
    print "%s [interface] [dest_mac] [dest_ip] [time(seconds)]" % (sys.argv[0])

def millis(start_time):
    """Returns milliseconds elapsed since start_time"""
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def main():
    if len(sys.argv) != 5:
        usage()
        sys.exit()

    interface = sys.argv[1]
    dest_mac = sys.argv[2]
    dest_ip = sys.argv[3]
    seconds = int(sys.argv[4])

    start_time = datetime.now()
    timestamps = []

    def packet_handler(packet):
        if packet[ARP].hwdst == dest_mac and \
           packet[ARP].pdst == dest_ip:
            timestamps.append(millis(start_time));

    arp.sniff_arp_packets(callback=packet_handler,
                          timeout=seconds)

    pp.plot(timestamps, len(timestamps)*[1], "x")
    pp.xlabel("Timestamps")
    pp.ylabel("Packets receive count")
    pp.savefig('receive_packets_output.png')

    print "%d packets received" % len(timestamps)

if __name__ == '__main__':
    main()
