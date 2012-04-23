#!/usr/bin/env python

import socket
import os
import shlex
from subprocess import Popen
from subprocess import PIPE

host = ''
port = 3210
backlog = 0
size = 1024

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

s.bind((host,port))
s.listen(backlog)

client, address = s.accept()
try:
	while 1:
		data = client.recv(size)
		strdata = shlex.split(data)
		if len(strdata):
			if (strdata[0] == "cd"):
				os.chdir(strdata[1])
			elif (strdata[0] == "cat"):
				client.send(open(strdata[1]))
			elif (strdata[0] == "ls" and len(strdata) == 2):
				client.send("\n".join(os.listdir(strdata[1]))+"\n")
			elif (strdata[0] == "ls" and len(strdata) == 1):
				client.send("\n".join(os.listdir("."))+"\n")
finally:
	s.close()
