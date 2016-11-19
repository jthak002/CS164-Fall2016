def fb_passwdchng (uname, new_passwd):
	#creating empty lists
	new_passwd=new_passwd+'\n'
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
		pass_list[uname_list.index(uname)]=new_passwd
	else: 
		pass
	upass.close()
	upass = open('upass.txt','w')
	for i in range(0,len(uname_list)):
		upass.write(uname_list[i] + '\t' + pass_list[i])
	upass.close()

