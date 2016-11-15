import os
import sys
import socket
from check import ip_checksum
import select

try:
	s=socket.socket(socket.AF_INET, socket.SOCK_DGARM)
except socket.error:
	print 'Socket creation failed'
	sys.exit()
print 'socket created'

host='localhost'
port=5000
inputs = [sys.stdin, s]
outputs = [ ]
exception = [s]
print 'Please enter your messages + Press Enter'
while 1:
	readable,writable,excepts = select.select(inputs, outputs, exception)
	for x in readable:
		if x is sys.stdin:
			smh=sys.stdin.readline()
			smh=smh.strip()
			if smh == 'EXIT':
				s.close()
				sys.exit()
			else:
				print 'Sending Packet: '
				smh='0&'+ip_checksum(smh)+'&'+smh
				s.sendto(smh,(host, port))
				
			continue
		elif x is s:
			d=s.recvfrom(1024)
			data=d[0]
			addr=d[1]
			if data == 'ACK':
				print 'ACK RECVD'
			else:
				print 'ERR'
		continue
sys.exit()
			
