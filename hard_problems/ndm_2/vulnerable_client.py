#!/usr/bin/env python
# Echo client program
import socket
import sys

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while (True):
        s.send('password')
        data = s.recv(1024)
        print 'Received', repr(data)

def print_usage():
    sys.stderr.write("Usage:  " + sys.argv[0] + " hostname [port]\n")

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1:
        print_usage()
        quit()
    elif argc == 2:
        host = sys.argv[1]
        port = 9125 
    elif argc == 3:
        host = sys.argv[1]
        port = sys.argv[2]
    else
        print('Invalid usage')
    main()
    s.close()
