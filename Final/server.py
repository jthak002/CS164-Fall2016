import socket
import os
import sys
from thread import*
from authen import ip_authen
HOST ='' #blank space to ask the socket 
		 #to bind on all available interfacea
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
	s.bind((HOST,PORT)) 
except socket.error:
	print 'socket bind failed'
	sys.exit()
print 'socket bind complete'

#start listening on socket - Persistent TCP connection
s.listen(10)
print 'socket listening'
login =False
#Thread function to handle connections
def clientthread(conn):
	#sending welcome message to client server
	conn.send(' Welcome to facebook\nPlease enter your Username and Password')
	
	#Waiting for client feedback
	while 1:
		data=conn.recv(1024)
		print '[' + addr[0] + ':' + str(addr[1]) + '] ' + data
		data_split = data.split(' ', 4)
		if ip_authen(data_split[1],data_split[3]):
			print 'Authentication Successful'
			conn.send('True') #replace with a tougher ACK
			login=True
			break
		else:
			conn.send('False') #replace with tougher NACK
			print 'Authentication Unsuccessful'
	conn.close()

#waiting for client connections
while 1:
	conn,addr = s.accept()
	print 'connected to client:' + addr[0] + ':' + str(addr[1])
	#start thread to create association with client
	start_new_thread(clientthread, (conn,))
s.close()
