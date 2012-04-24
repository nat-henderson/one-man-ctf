#!/usr/bin/env python
import smtpd
import email
import smtplib
import socket
import asyncore
import platform
mydomain = platform.node() or 'localhost'
acceptedaddr="foobar@%s" % mydomain
sentto="password-recovery@%s" % mydomain
passwd="baz"
mailserver = 'smtp.case.edu'
class MySMTP(smtpd.SMTPServer) :
	def __init__(self, localaddr, remoteaddr) :
		smtpd.SMTPServer.__init__(self,localaddr, remoteaddr)

	def process_message(self,peer, mailfrom, rcpttos, data) :
		if sentto in rcpttos :
			#it was sent to the right address
			send_password(mailfrom, data) 

def send_password(mailfrom, data) :
	message = email.message_from_string(data) 
	#set the response
	if 'From' in message and message['From'] == acceptedaddr :
		response = "Thank you for using the Woozits password recovery\n" + \
			"Service. Your password is %s" % passwd
	else :
		response = "Account not Found"
	
	#set the "to" addr
	if 'Reply-To' in message:
		to = message['Reply-To']
	else:
		to = mailfrom
	#if we're replying, set the message ID
	headers={}
	if 'Message-ID' in message :
		headers['In-Reply-To'] = message['Message-ID']
	headers['From'] = "Password Recovery Service <%s>" % sentto
	#generate the message
	msg_header = '\n'.join(("%s:%s" % (key, value)) for key,value in headers.iteritems())
	data = msg_header + "\n" + response
	#send the email
	print "TO: %s" % to
	print 'DATA: %s' % data
	conn = smtplib.SMTP(mailserver)
	i = 3
	while i :
		try :
			foo = conn.sendmail(sentto, to, data)
			break;
		except smtplib.SMTPRecipientsRefused as e:
			print 'error connecting. retrying'
			i-=1
	print foo
	conn.quit()

x = MySMTP(("localhost",25),None)

asyncore.loop()
