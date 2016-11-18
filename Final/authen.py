def ip_authen (uname, passwd):
	#creating empty lists
	passwd=passwd+'\n'
	uname_list=[]
	pass_list=[]
	#populating list with username and passwords 
	try:	
		upass = open('upass.txt','r')
	except IOError:
		print 'could not read file'
		sys.exit()
	for line in upass:
		line_split=line.split('\t',2)
		uname_list.append(line_split[0])
		pass_list.append(line_split[1])
	if uname in uname_list:
		#print 'passwd ' + passwd + ' pass_list: ' + pass_list[uname_list.index(uname)]
		return passwd == pass_list[uname_list.index(uname)]
	else: 
		return False

