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

#LANDING PAGE--SPLASH SCREEN
print 'Hey, ' + uname
#RECV menu items
menu=s.recv(1024)	
while 1:
	print menu
	menu_choice=raw_input('Menu choice: ')	#Menu Options
	s.send(menu_choice)			#Sending user choice to server
	
	#_________CHANGE_PASSWORD____________
	if menu_choice == 'change password':
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
	#_________LOGOUT___________
	elif menu_choice == 'logout':
		print 'logging out...'
		os.system('clear')
		break
	#________INVALID_ENTRIES_____
	else:
		print 'Invalid choice'
		continue
s.close()
