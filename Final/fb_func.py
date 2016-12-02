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
#________!FINDING IF USERNAME EXISTS___________
def fb_frndexists(uname):
	uname=uname.strip()
	unames=[]
	try:
		fileio=open('upass.txt', 'r')
	except IOError:
		print 'UPASS ERROR'
		sys.exit()
	for line in fileio:
		data=line.split('\t',2)
		unames.append(data[0])
	fileio.close()
	if uname in unames:
		del unames[:]
		return True
	else:
		del unames[:]
		return False
#________!FINDING IF USERNAME EXISTS IN PENDING FRIEND REQUESTS OF FUNAME___________
def fb_chckpfrndlist(funame,uname):
	filename='Friends/'+funame+'_pflist.txt'
	unames=[]
	try:
		fileio=open(filename, 'r')
	except IOError:
		print 'PLIST ERROR'
		sys.exit()
	for line in fileio:
		unames.append(line.strip())
	fileio.close()
	if uname in unames:
		del unames[:]
		return True
	else:
		del unames[:]
		return False
#_________!SENDING FRIEND REQUEST!_______________
def fb_addfrnd(uname,funame):
	filename='Friends/'+funame+'_pflist.txt'
	try:
		fileio=open(filename,'a')
	except IOError:
		print 'PLIST CORRUPT'
		sys.exit()
	fileio.write(uname+'\n')
	fileio.close()
#_______COUNT PENDING FRIEND REQUESTS____________
def fb_countpfrnd(uname):
	filename='Friends/'+uname+'_pflist.txt'
	count=0
	try:
		fileio=open(filename,'r')
	except IOError:
		print 'PLIST CORRUPT'
		sys.exit()
	for line in fileio:
		count=count+1
	fileio.close()
	return count
#__________Retrieve friend plist_________________
def fb_rtrvplist(uname):
	filename='Friends/'+uname+'_pflist.txt'
	plist_cntnt=[]
	try:
		fileio=open(filename,'r')
	except IOError:
		print 'PLIST CORRUPT'
		sys.exit()
	for line in fileio:
		plist_cntnt.append(line.strip())
	fileio.close()
	return plist_cntnt
#_____________ADDING FRIEND______________________
def fb_acceptfrnd(uname, funame):
	filename='Friends/'+uname+'_pflist.txt'
	unames_kill=[]
	try:
		fileio=open(filename,'r')
	except IOError:
		print 'PLIST Error'
		sys.exit()
	for line in fileio:
		unames_kill.append(line.strip())
	print unames_kill
	unames_kill.remove(funame)
	fileio.close()
	try:
		fileio=open(filename,'w')
	except IOError:
		print 'PLIST CORRUPT'
		sys.exit()
	for line in unames_kill:
		fileio.write(line+'\n')
	fileio.close()
	del unames_kill[:]

	filename = 'Friends/'+uname+'_flist.txt'
	try:
		fileio=open(filename,'a')
	except IOError:
		print 'FLIST Error'
		sys.exit()
	fileio.write(funame+'\n')
	fileio.close()
	filename='Friends/'+funame+'_flist.txt'
	try:
		fileio=open(filename,'a')
	except IOError:
		print 'FLIST corrupted'
		sys.exit()
	fileio.write(uname+'\n')
	fileio.close()	
#______________!Reject FRiend Request___________
def fb_rejectfrnd(uname, funame):
	filename='Friends/'+uname+'_pflist.txt'
	unames_kill=[]
	try:
		fileio=open(filename,'r')
	except IOError:
		print 'PLIST Error'
		sys.exit()
	for line in fileio:
		unames_kill.append(line.strip())
	print unames_kill
	unames_kill.remove(funame)
	fileio.close()
	try:
		fileio=open(filename,'w')
	except IOError:
		print 'PLIST CORRUPT'
		sys.exit()
	for line in unames_kill:
		fileio.write(line+'\n')
	fileio.close()
	del unames_kill[:]


