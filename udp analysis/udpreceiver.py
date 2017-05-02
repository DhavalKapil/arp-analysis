import socket
import netifaces
import sys
import time
from datetime import datetime
import random

def millis(start_time):
    """Returns milliseconds elapsed since start_time"""
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

interface = sys.argv[1]
seconds = 14

addresses = netifaces.ifaddresses(interface)
server_ip = addresses[netifaces.AF_INET][0]['addr']

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ((server_ip, 10000))
sock.bind(server_address)

start_time = datetime.now()
count = 0 

while millis(start_time) < seconds*1000:
    data, address = sock.recvfrom(4096)
    count += 1
    #print 'received %s bytes from %s' % (len(data), address)
    #print data

print count