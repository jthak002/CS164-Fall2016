import os
import sys
import datetime
#______________Accessing user messages_______________
def fb_mssgs(uname):
	new_messg=[]
	old_messg=[]
	#populating the lists with new and old password
	filename='Messages/'+uname+'_new.txt'
	#populating the new messages first
	try:
		fileio=open(filename,'r+')
	except IOError:
		print 'Message Database Corrupted'
		sys.exit()
	for line in fileio:
		new_messg.append(line)
	#Emptying the contents of the file
	fileio.seek(0)
	fileio.truncate()
	fileio.close() #file closed
	#reversing the new messages as they're placed at the bottom when the arrive
	new_messg.reverse()

	#retrieving old messages 
	filename='Messages/'+uname+'_old.txt'
	try:
		fileio=open(filename,'r+')
	except IOError:
		print 'Message Database Corrupted'
		sys.exit()
	for line in fileio:
		old_messg.append(line)		
	#PREPENDING NEW MESSAGES ONTO OLD MESSAGES DATA FILE
	fileio.seek(0)
	fileio.truncate()
	for line in new_messg:
		fileio.write(line)
	for line in old_messg:
		fileio.write(line)
	fileio.close()
	return [new_messg, old_messg]
#_____________!COUNTING NUMBER OF NEW MESSAGES__________
def fb_mssgcnt(uname):
	count=0
	filename='Messages/'+uname+'_new.txt'
	try:
		fileio=open(filename,'r')
	except IOError:
		print 'Message Database Corrupted'
		sys.exit()
	for line in fileio:
		count=count+1
	return count if count>0 else 0
#_____________!Check Friend List!______________
def fb_chckfrndlist(uname, frndname):
	frndlst=[]
	filename='Friends/' + uname + '_flist.txt'
	try:
		fileio=open(filename, 'r+')
	except IOError:
		print 'Friend List Corrupted'
		sys.exit()
	for line in fileio:
		frndlst.append(line.strip())
	for line in frndlst:
		if line == frndname:
			return True
	return False
#_____________!MESSAGE DELIVERY!_______________
def fb_msgdlvry(frndname, uname, msg):
	filename='Messages/'+frndname+'_new.txt'
	try:
		fileio=open(filename, 'a')
	except IOError:
		print 'Message File Corrupted'
		sys.exit()
	msg=uname + ' [' + str(datetime.datetime.now()) + ']: ' + msg +'\n'
	fileio.write(msg)
	fileio.close()
