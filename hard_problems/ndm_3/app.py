#!/usr/bin/env python
from cgi import escape
import sys, os, subprocess
import binascii, urlparse
import random
import MySQLdb as mdb
from flup.server.fcgi import WSGIServer

def make_link(query):
    while True:
	short = binascii.hexlify(os.urandom(6))
	url = query[2:]
	cur.execute("SELECT * FROM urls WHERE longurl='%s'" % url)
	data = cur.fetchall()
	if len(data) == 0:
	    cur.execute("SELECT * FROM urls WHERE short='%s'" % short)
	    data = cur.fetchall()
	    if len(data) == 0:
		cur.execute("INSERT INTO urls VALUES('%s', '%s')" % (short, url))
		data = cur.fetchall()
		return '<a href="/app.py?q=%s">Your obfuscated URL is here.</a>' % short
	else:
	    return '<a href="/app.py?q=%s">Your obfuscated URL is here.</a>' % data[0][0]


def follow_link(query):
    short=query[2:]
    cur.execute("SELECT * FROM urls WHERE short='%s'" % con.escape_string(short))
    data = cur.fetchall()
    if len(data) > 0 and len(data[0]) > 0:
	return '<meta http-equiv="REFRESH" content="0;url=%s">' % data[0][1]


def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    query = environ['QUERY_STRING']
    if len(query) > 0:
        if query[0] == 'a':
	    try:
	    	s = make_link(query) 
	    	yield s
	    except mdb.OperationalError:
		setup()
		s = make_link(query)
		yield s
	elif query[0] == 'q':
	    try:
		s = follow_link(query)
		yield s
	    except mdb.OperationalError:
		setup()
		s = follow_link(query)
		yield s

con = None
cur = None

def setup():
    try:
    	global con
	global cur
	con = mdb.connect(user='root', db='shortener', read_default_file="/usr/.my.cnf");
	cur = con.cursor()
    except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

setup()
WSGIServer(app).run()
