import socket
import os
import sys
import threading
from thread import*
from authen import ip_authen
from passwdchng  import fb_passwdchng
from fb_func import*

#CONSTANTS
HOST ='' #blank space to ask the socket 
		 #to bind on all available interfacea
PORT= 5000 #HOST port can be random
noNewMsg='No Unread Messages'
SEMAMSG=1
#END of LIST OF CONSTANTS
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
uname=''
msg_pool = threading.Semaphore(SEMAMSG)
#Thread function to handle connections
def clientthread(conn):
	#sending welcome message to client server
	conn.send('Welcome to facebook\nPlease enter your Username and Password')
	
	#Waiting for client feedback
	while 1:
		data=conn.recv(1024)
		print '[' + addr[0] + ':' + str(addr[1]) + '] ' + data
		data_split = data.split(' ', 4)
		if ip_authen(data_split[1],data_split[3]):
			uname=data_split[1]
			print 'Authentication Successful'
			conn.send('ACKNOWLEDGETrueLOGIN123456789') #replace with a tougher ACK
			login=True
			break
		else:
			conn.send('False') #replace with tougher NACK
			print 'Authentication Unsuccessful'
	waste=conn.recv(1024)	#Python couples the ACKnowledgement and menu in one packet
							#hence, flushing the sockets buffer 	
	while login:
		menu='1.change password\n2.logout\n3.messages (' + str(fb_mssgcnt(uname)) + ')\n4.send messages'
		conn.send(menu)
		print 'Menu intiated'
		menu_choice=conn.recv(1024)
		if (menu_choice =='change password' or menu_choice =='1'):
			print 'Change passwd'
			uname=conn.recv(1024)
			new_passwd=conn.recv(1024)
			fb_passwdchng(uname,new_passwd)
			continue
		elif (menu_choice == 'logout' or menu_choice == '2'):
			print 'logging out..'
			login=False
		elif (menu_choice == 'messages' or menu_choice == '3'):
			print 'Messages'
			#receive a list with a list of new messages and old messages
			msg_pool.acquire()		#Using semaphores to preserve integrity
									#of text files in Messages
			mssg_data = fb_mssgs(uname)
			msg_pool.release()
			new_msg=mssg_data[0]
			old_msg=mssg_data[1]
			text='______Unread Messages______\n'
			for line in new_msg:
				text=text+line
			text=text+'________Read Messages_______\n'
			for line in old_msg:
				text=text+line
			conn.send(text)
			conf=conn.recv(1024)
			print conf
		elif (menu_choice =='send messages' or menu_choice == '4'):
			print 'Send Messages..Querying friend_name'
			frndname=conn.recv(1024)
			isfrnd=fb_chckfrndlist(uname, frndname)
			conn.send(str(isfrnd))
			if isfrnd:
				msg=conn.recv(4096)
				msg_pool.acquire()
				fb_msgdlvry(frndname,uname,msg)
				msg_pool.release()
			else:
				print 'NFE-----'
				conn.recv(1024)
				continue
		else:
			print 'Invalid choice'
	print 'fin'
	conn.close()

#waiting for client connections
while 1:
	conn,addr = s.accept()
	print 'connected to client:' + addr[0] + ':' + str(addr[1])
	#start thread to create association with client
	start_new_thread(clientthread, (conn,))
s.close()
