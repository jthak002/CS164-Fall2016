import os
import sys
import socket
import select

HOST='127.0.0.1'
PORT=5000

inputs = [sys.stdin]
outputs = [ ]
exception = [ ]

while 1:
	readable,writable,excepts = select.select(inputs, outputs, exception)
	for x in readable:
		if x is sys.stdin:
			smh=sys.stdin.readline()
			smh=smh.strip()
			if smh == 'EXIT':
				sys.exit()
			else:
				print smh
			continue
sys.exit()
			
