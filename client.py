#!/usr/bin/env python  

import socket
import threading
import signal
import sys  

class Client:

	def __init__(self):

		# self.config = config
		signal.signal(signal.SIGINT, self.shutdown) 
		self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.Socket.bind(("127.0.0.1", 20000))


	def shutdown(self, signum, frame):
		self.Socket.close()
		sys.exit(0)

	def takeInput1(self):
		print "enter client port server port and get/post"
		cmd1 = raw_input()  
		cmd1 = cmd1.split() 
		# print cmd1[2]
		self.SendRequest(cmd1[1],cmd1[2])

	def SendRequest(self, cmd ,get):
		if get == '1':
			request = 'POST localhost:' + cmd + ' HTTP/1.1\n'
			request += 'Host: localhost:' + cmd
			request += '\nAccept-Encoding: gzip, deflate\n'
			request += 'Connection: keep-alive\n\n'
		else:
			request = 'GET localhost:' + cmd + ' HTTP/1.1\n'
			request += 'Host: localhost:' + cmd
			request += '\nAccept-Encoding: gzip, deflate\n'
			request += 'Connection: keep-alive\n\n'
			

		# print request
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.settimeout(5)
		s.connect(('127.0.0.1', 20100))
		s.sendall(request)
		cnt = 0

		try:
			for i in range(10):
				msg = s.recv(1024)
				if msg[len(msg) - 1] == '$':
					print msg[:-1]
				print msg
				# print "lol"
				# inpflag = 1
				
				if msg == 'Enter username and password with a space between them\n':
					# print "ok"
					cmd = raw_input()
					# print cmd
					s.sendall(cmd)
		except:
			pass


if __name__ == "__main__":

	client = Client()
	if (len(sys.argv) < 4):
		print "Format - python2 client.py <client port> <server port> <get(0) or post(1)>"
		# break
	else:
		get = int(sys.argv[3])
		cmd = sys.argv[2]  
		cport = int(sys.argv[1])
		# print cmd
		# print get
		client.SendRequest(cmd,get)
		# print "lol"
	client.takeInput1()
	while True:
		client.takeInput1()