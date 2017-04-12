import netifaces
import sys
import time
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pp

from lib import arp

def usage():
    print "Usage:"
    print "%s [interface] [time(seconds)]" % (sys.argv[0])

def millis(start_time):
    """Returns milliseconds elapsed since start_time"""
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit()

    interface = sys.argv[1]
    seconds = int(sys.argv[2])

    addresses = netifaces.ifaddresses(interface)
    src_mac = addresses[netifaces.AF_LINK][0]['addr']
    src_ip = addresses[netifaces.AF_INET][0]['addr']

    dest_mac = "55:55:55:55:55:55" # dummy MAC
    dest_ip = "5.5.5.5" # dummy IP

    start_time = datetime.now()
    timestamps = []

    while millis(start_time) < seconds*1000:
        packet = arp.create_arp_packet(src_mac,
                                       src_ip,
                                       dest_mac,
                                       dest_ip,
                                       arp.ARP_REPLY)
        arp.send_arp_packet(packet)
        timestamps.append(millis(start_time))

    pp.plot(timestamps, len(timestamps)*[1], "x")
    pp.savefig('flood_packets_output.png')

    print "%d reply packets send" % len(timestamps)
    print "Each packet has size: 28(ARP header) + 14(Ethernet header) bytes= 42"
    print "Transmission rate: %f bytes/second" % (len(timestamps)*42.0/seconds)

if __name__ == '__main__':
    main()

