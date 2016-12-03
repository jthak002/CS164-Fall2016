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
data_pool = threading.Semaphore(SEMAMSG)
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
		menu='1.change password\n2.logout\n3.messages (' + str(fb_mssgcnt(uname)) + ')\n4.send messages\n5.send friend request\n6.pending friend requests('+str(fb_countpfrnd(uname))+')\n7.enter your status update\n8.timeline\n9.news feed\n0.refresh'
		conn.send(menu)
		print 'Menu intiated'
		menu_choice=conn.recv(1024)
		#__________________CHANGE PASSWORD________________________
		if (menu_choice =='change password' or menu_choice =='1'):
			print 'Change passwd'
			uname=conn.recv(1024)
			new_passwd=conn.recv(1024)
			data_pool.acquire()
			fb_passwdchng(uname,new_passwd)
			data_pool.release()
			continue
		#____________________LOGOUT_________________________
		elif (menu_choice == 'logout' or menu_choice == '2'):
			print 'logging out..'
			login=False
		#________________MESSAGES______________________________
		elif (menu_choice == 'messages' or menu_choice == '3'):
			print 'Messages'
			#receive a list with a list of new messages and old messages
			data_pool.acquire()		#Using semaphores to preserve integrity
									#of text files in Messages
			mssg_data = fb_mssgs(uname)
			data_pool.release()
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
		#!__________________SEND MESSAGES__________________________
		elif (menu_choice =='send messages' or menu_choice == '4'):
			print 'Send Messages..Querying friend_name'
			frndname=conn.recv(1024)
			data_pool.acquire()
			isfrnd=fb_chckfrndlist(uname, frndname)
			data_pool.release()
			conn.send(str(isfrnd))
			if isfrnd:
				msg=conn.recv(4096)
				data_pool.acquire()
				fb_msgdlvry(frndname,uname,msg)
				data_pool.release()
			else:
				print 'NFE-----'
				conn.recv(1024)
				continue
		#________________SEND FRIEND REQUESTS_____________________________
		elif (menu_choice == 'Send Friend Requests' or menu_choice == '5'):
			funame=conn.recv(1024)	#Receive the username to send friend request to
			#check for the following things before sending friend request
			#1.if the username is a member on facebook
			#2.if the the username is already friends with the currently logged in user
			#3.if the username is not equal to the currently logged in user
			#i.e. the user isn't trying to send a friend request to himself
			#4. Avoid sending duplicate friend requests
			data_pool.acquire()
			conf=fb_frndexists(funame) and not fb_chckfrndlist(uname,funame) and not uname == funame and not fb_chckpfrndlist(funame,uname)
			data_pool.release()
			conn.send(str(conf)) #checking if user exists or friends already in the list
			print uname
			if conf:
				data_pool.acquire()
				fb_addfrnd(uname,funame)
				data_pool.release()
				print 'friend added'
			conn.recv(1024)

		#_________________ACCEPT FRIEND REQUESTS__________________________
		elif (menu_choice=='Pending Friend Requests' or menu_choice =='6'):
			textdata=''
			data_pool.acquire()
			plist_cntnt=fb_rtrvplist(uname)
			data_pool.release()
			for line in plist_cntnt:
				textdata=textdata+line+'\n'
			if textdata == '':	#incase of empty pflist
				textdata='empty'
				conn.send(textdata)
				conn.recv(1024)	#Garbage value
				continue
			conn.send(textdata.strip())
			s=conn.recv(1024)
			s_split=s.split()
			if(len(s_split) is 2):
				if s_split[0] == 'accept':
					data_pool.acquire()
					fb_acceptfrnd(uname,s_split[1].strip())
					data_pool.release()
					conn.send(s_split[1]+'\'s friend request has been accepted')
				else:
					data_pool.acquire()
					fb_rejectfrnd(uname,s_split[1].strip())
					data_pool.release()
					conn.send(s_split[1]+'\'s friend request has been rejected')
			else:
				conn.send('no changes have occured') 
			conn.recv(1024)
			continue
		#_________________POST A STATUS UPDATE___________________________
		elif (menu_choice =='post a status update' or menu_choice =='7'):
			textdata=conn.recv(1024)
			data_pool.acquire()
			fb_poststatus(uname,textdata)
			data_pool.release()
		#__________________ DISPLAY TIMELINE______________________________
		elif (menu_choice =='timeline' or menu_choice == '8'):
			data_pool.acquire()
			temp_data=fb_tlinedisplay(uname)
			data_pool.release()
			conn.send(temp_data)
			conn.recv(1024)
		#___________________DISPLAY WALL__________________________________
		elif (menu_choice =='wall' or menu_choice =='9'):
			data_pool.acquire()
			num_list,post_list=fb_newsfeed(fb_rtrvflist(uname))
			data_pool.release()
			if len(num_list) ==0:
				conn.send("no Posts to show")
			else:
				dictionary=dict(zip(num_list,post_list))
				text=''
				for key in dictionary:
					text=text+dictionary[key]+'\n'
				conn.send(text)
			conn.recv(1024)
		elif (menu_choice=='refresh' or menu_choice=='0'):
			conn.recv(1024)
		#_________________INVALID MENU CHOICE_________________________		
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
