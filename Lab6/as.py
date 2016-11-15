import os
import sys
import socket
import select
from check import ip_checksum


HOST=''
PORT=5000
try:
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
	print 'Socket bind failed'
	sys.exit()
print 'Socket Created'

try:
	s.bind((HOST,PORT))
except socket.error:
	print 'Socket bind Failed'
	sys.exit()
print 'Socket Bind Complete'

while 1:
	da=s.recvfrom(1024)
	d=da[0]
	addr=da[1]
	data=d.split('&',3)
	if (data[0]=='0' and ip_checksum(data[2])==data[1]):
		print '[' + addr[0] + ':' + str(addr[1]) + '] -' + data[2]
		ack='ACK'
		s.sendto(ack,(addr[0],addr[1]))
	else:
		print '[' + addr[0] + ':' + str(addr[1]) + '] - PACK_ERR'
		ack='NACK'
		s.sendto(ack,(addr[0],adr[1]))
	continue
s.close()
