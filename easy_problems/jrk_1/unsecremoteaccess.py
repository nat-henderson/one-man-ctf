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
hasuser = True

try:
	while 1:
		client, address = s.accept()
		hasuser = True
		while hasuser:
			data = client.recv(size)
			strdata = shlex.split(data)
			if len(strdata):
				try:
					if (strdata[0] == "cd"):
						os.chdir(strdata[1])
					elif (strdata[0] == "cat"):
						client.send(open(strdata[1]).read())
					elif (strdata[0] == "ls" and len(strdata) == 2):
						client.send("\n".join(os.listdir(strdata[1]))+"\n")
					elif (strdata[0] == "ls" and len(strdata) == 1):
						client.send("\n".join(os.listdir("."))+"\n")
					elif (strdata[0] == "exit" or strdata[0] == "quit"):
						client.close()
						hasuser = False
				except OSError,IOError:
					client.send("Permission Denied.\n")
finally:
	s.close()
