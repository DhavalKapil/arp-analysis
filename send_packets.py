import netifaces
import sys
import time
from datetime import datetime
import random

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

    addresses = netifaces.ifaddresses(interface)
    src_mac = addresses[netifaces.AF_LINK][0]['addr']
    src_ip = addresses[netifaces.AF_INET][0]['addr']

    start_time = datetime.now()
    timestamps = []
    while millis(start_time) < seconds*1000:
        packet = arp.create_arp_packet(src_mac,
                                       src_ip,
                                       dest_mac,
                                       dest_ip,
                                       arp.ARP_REQUEST)
        arp.send_arp_packet(packet)
        timestamps.append(millis(start_time))

        # Sleep for a random amount of time
        time.sleep(random.uniform(0, 2.0))

    pp.plot(timestamps, len(timestamps)*[1], "x")
    pp.xlabel("Timestamps")
    pp.ylabel("Packets sent count")
    pp.savefig('send_packets_output.png')

    print "%d packets send" % len(timestamps)

if __name__ == '__main__':
    main()
