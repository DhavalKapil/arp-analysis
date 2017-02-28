import netifaces
import sys
import time
import random

import arp

def usage():
    print "Usage:"
    print "%s [interface] [dest_mac] [dest_ip] [time(seconds)]" % (sys.argv[0])

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

    start_time = time.time()
    while time.time() < (start_time + seconds):
        packet = arp.create_arp_packet(interface,
                                       src_mac,
                                       src_ip,
                                       dest_mac,
                                       dest_ip,
                                       arp.ARP_REQUEST)
        arp.send_arp_packet(packet)

        # Sleep for a random amount of time
        time.sleep(random.uniform(0, 2.0))

if __name__ == '__main__':
    main()
