#!/usr/bin/env python
import smtpd
import email
import smtplib
import socket
import asyncore
import platform
mydomain = 'ec2-107-20-71-239.compute-1.amazonaws.com'
acceptedaddr="level03@%s" % mydomain
sentto="password-recovery@%s" % mydomain
passwd="M6DH3&MA9.#wUcuioiLT"
mailserver = 'smtp.case.edu'

authorized_ips = ('10.196.81.248',)
class MySMTP(smtpd.SMTPServer) :
	def __init__(self, localaddr, remoteaddr) :
		smtpd.SMTPServer.__init__(self,localaddr, remoteaddr)

	def process_message(self,peer, mailfrom, rcpttos, data) :
		if peer not in authorized_ips :
			print peer + " is not authorized"
			return
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
			foo = conn.sendmail('password-recovery@case.edu', to, data)
			break;
		except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSendersRefused) as e:
			print 'error connecting. retrying'
			i-=1
	print foo
	conn.quit()

x = MySMTP(("129.22.21.164",8020),None)

asyncore.loop()
