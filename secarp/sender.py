import netifaces
import sys
import time
from datetime import datetime

from lib import arp

def usage():
    print "Usage:"
    print "%s [src_ip] [src_mac] [dest_ip] [dest_mac] [time(seconds)]" \
        % (sys.argv[0])

def millis(start_time):
    """Returns milliseconds elapsed since start_time"""
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

def main():
    if len(sys.argv) != 6:
        usage()
        sys.exit()

    src_ip = sys.argv[1]
    src_mac = sys.argv[2]
    dest_ip = sys.argv[3]
    dest_mac = sys.argv[4]
    seconds = int(sys.argv[5])

    start_time = datetime.now()

    while millis(start_time) < seconds*1000:
        packet = arp.create_arp_packet(src_mac,
                                       src_ip,
                                       dest_mac,
                                       dest_ip,
                                       arp.ARP_REPLY)
        arp.send_arp_packet(packet)

if __name__ == "__main__":
    main()
