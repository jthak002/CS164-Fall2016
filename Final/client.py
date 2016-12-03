import socket
import os
import sys
from thread import*
import getpass

HOST ='10.0.0.4' #server ip -can be replaced with the canonical name
PORT= 5000 #HOST port can be random
login=False
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
	print 'SERVER UNREACHABLE -- ERROR'
	sys.exit()
print 'now connected to facebook'

print s.recv(4096)
#client connected to server
while not login:
	#authentication
	uname=raw_input('username: ')		#getting username
	passwd=getpass.getpass('password: ')	#getting the password via getpass
						#UNIX terminal like password input
	data='Username: ' + uname + ' Password: ' + passwd	
	#compiling username and password int o one packet
	try:
		#sending login details to server app
		s.send(data)	
	except socket.error:
		#send data fail
		print 'Authentication Error - login details not sent'
		sys.exit()
	reply=s.recv(1024)
	#print reply--TEST CASE to check for server reply
	if reply == 'ACKNOWLEDGETrueLOGIN123456789':	
		#complex login authentication
		s.send('waste')	
		#sending a waste value to flush the socket buffer
		login=True	
		#setting global bool value for login
		break
		#--functions work as long as login=True
	else:
		print 'Authentication Unsuccessful. Please Try Again'
		continue

while 1:
	#LANDING PAGE--SPLASH SCREEN
	print 'Hey, ' + uname
	#Received menu items
	menu=s.recv(1024)
	print menu
	menu_choice=raw_input('Menu choice: ')	#Menu Options
	s.send(menu_choice)			#Sending user choice to server
	
	#_________CHANGE_PASSWORD____________
	if (menu_choice == 'change password' or menu_choice == '1'):
		curr_passwd=getpass.getpass('current password    : ')
		new_passwd=getpass.getpass('new password        : ')
		conf_passwd=getpass.getpass('confirm new password: ')#check for various requirements
		#print curr_passwd + ' ' + new_passwd + ' ' + conf_passwd + ' '+ passwd 
		#TEST CASE--Check for correct input > New password = Confirm new password
		if( curr_passwd==passwd and conf_passwd == new_passwd and len(conf_passwd)>3):
			s.send(uname)	#change password with associated username
			s.send(conf_passwd)
			print 'Password Successfully Changed'
		else:
			#------!IMPROVE!----------
			s.send(uname)	#change to same password - Done to reduce coding by me
			s.send(passwd)	#but increases comp[utational load on server
			print'password unchanged'
			print'1.len has to be greater than 4'
			print'2.new password and confirmed password field should match'
	#_________LOGOUT___________________________________
	elif (menu_choice == 'logout' or menu_choice == '2'):
		print 'logging out...'
		os.system('clear')
		break
	#___________READ MESSAGES___________________________
	elif (menu_choice == 'messages' or menu_choice =='3'):
		print 'Hey, ' + uname + '! Here are your messages.'
		data=s.recv(1024)
		print data
		s.send('messages received')
	#___________SEND MESSAGES_________________________________
	elif (menu_choice == 'send messages' or menu_choice == '4'):
		frndname=''
		while frndname=='':
			frndname=raw_input('Enter Friend\'s name: ')
		s.send(frndname)
		if s.recv(1024) == 'True':
			msg=''
			while (msg==''):
				msg=raw_input('Enter Your Message: ')
			s.send(msg)
		else:
			s.send('garbage value')
			continue
	elif (menu_choice =='Send Friend Requests' or menu_choice =='5'):
		funame=''
		while funame == '':
			funame=raw_input('Enter Friend\'s Username: ')
		funame=funame.strip()
		s.send(funame)
		conf=s.recv(1024)
		if conf == 'True':
			print 'Friend Request Sent'
		else:
			print 'Friend Request Not Sent\n1.Invalid Username OR\n2.Friend Request Already Sent'
		s.send('garbage value')
		  
	elif (menu_choice =='Pending Friend Requests' or menu_choice =='6'):
		print'Here are your pending friend requests:'
		pflist=s.recv(1024)
		if pflist == 'empty':
			print 'No pending friend requests'
			s.send('garbage value')	#continue here
			continue				#start menu again
		print pflist
		d_list=pflist.split('\n')
		print 'Enter \'accept\' or \'reject\' followed by username to accept or reject friend request or \'exit\' to go back to the main menu'
		while 1:	#waiting to receive proper input
			resp=raw_input()
			if resp =='exit':
				s.send('exit')
				print s.recv(1024)
				break
			pfr=resp.split(' ')
			if len(pfr)==2:
				if ((pfr[0] == 'accept' or pfr[0]=='reject') and pfr[1].strip() in d_list):
					s.send(pfr[0]+' '+pfr[1].strip())
					print s.recv(1024) #receive cofirmation
					break
				else:
					print'Invalid entry. please try again'
			else:
				print'Invalid entry. please try again'
		s.send('garbage value')
	#________POST A STATUS UPDATE________________________________
	elif(menu_choice == 'post a status update' or menu_choice =='7'):
		text_data=''
		while text_data == '':
			text_data=raw_input('enter a status update: ')
		s.send(text_data)
	#________TIMELINE____________________________________________	
	elif(menu_choice =='timeline' or menu_choice == '8'):
		print s.recv(1024)
		s.send('garbage value')
	#________TIMELINE____________________________________________	
	elif(menu_choice =='newsfeed' or menu_choice == '9'):
		print '!_________________NEWS FEED__________________!'
		print s.recv(1024)
		s.send('garbage value')
	elif(menu_choice =='refresh' or menu_choice =='0'):
		s.send('garbage value')
	#________INVALID_ENTRIES_____
	else:
		print 'Invalid choice'
		continue
s.close()
