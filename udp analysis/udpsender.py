import socket
import netifaces
import sys
import time
from datetime import datetime
import random
# addressing information of target

def millis(start_time):
    """Returns milliseconds elapsed since start_time"""
    dt = datetime.now() - start_time
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    return ms

interface = sys.argv[1]
dest_ip = sys.argv[2]
seconds = int(sys.argv[3])

addresses = netifaces.ifaddresses(interface)
src_ip = addresses[netifaces.AF_INET][0]['addr']

PORTNUM = 10000
 
# enter the data content of the UDP packet as hex
PACKETDATA = 'f1a525da11f6'.decode('hex')
 
# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.bind((src_ip, 0))
# connect the socket, think of it as connecting the cable to the address location
s.connect((dest_ip, PORTNUM))

start_time = datetime.now()
count = 0 
try:
	while millis(start_time) < seconds*1000:
		# send the command
		s.send(PACKETDATA)
		time.sleep(0.2)
	 	count += 1
except:
	print count
print count
# close the socket
s.close()