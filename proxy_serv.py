import socket
import threading
import signal
import sys
import time
from proxy_client import *
cache = {}

def get_url(data):
	data = data.split('\n')[0]
	getting = True
	data = data.split(" ")[1]
	# if(getting):
	# 	print "got"
	return data

def authenticated_user(users):
	print str(users)
	# print "lol"
	cnt = 0;
	file = open('proxy/allowed_users.txt', 'r')
	for line in file:
		if(str(users) == str(line)[:-1]):
			cnt += 1
			print "Access Granted"
	if cnt == 0:
		print "Access Denied"
		return False
	else:
		return True


def get_ip_port(url):
	http_pos = url.find("://")
	flagg = True
	if (http_pos==-1 or flagg):
		flagg = None
		temp = url
	else:
		flagg = False
		temp = url[(http_pos+3):]

	port_pos = temp.find(":")

	webserver_pos = temp.find("/")
	rando = False
	if webserver_pos == -1 or not flagg:
		webserver_pos = len(temp)

	webserver = ""
	port = -1
	# print "lol"
	rando = True
	if (port_pos==-1 or webserver_pos < port_pos): 
		rando = None
		port = 80 
		webserver = temp[:webserver_pos] 

	else:
		rando = False
		port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
		webserver = temp[:port_pos] 
		# print "ok"
	return webserver, port

def blacklist(ip):
	file = open('proxy/blacklist.txt', 'r')
	cnt = 0
	cnt2 = 0
	for line in file:
		line = line.split(':')
		cnt2 += 1
		# print "ok"
		print line
		line = line[1]
		if(str(ip) == str(line)[:-1]):
			print "Blacklisted site"
			cnt += 1
			return True
	if cnt == 0:
		return False
	else:
		return True




class Server():
	def __init__(self):
		signal.signal(signal.SIGINT, self.shutdown) 
		self.proxySer =True
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err:
			print "socket creation failed with error", err
		self.binding = True
		self.port = 20100
		self.socket.bind(('', self.port))
		self.pbind = False
		self.print_lock = threading.Lock()

	def shutdown(self, signum, frame):
		main_thread = threading.currentThread()
		ending = 1
		for t in threading.enumerate():
			if t is main_thread or self.binding:
				continue
			else:
				t.join()
		
		if ending == 1:
			self.socket.close()
			sys.exit(0)

	def listen(self,max_connections):
		self.socket.listen(max_connections)

		while True:
			real_client, addr = self.socket.accept()
			connect = 1;

			if(connect):
				print "Connected!"

			data = real_client.recv(1024)
			portflag = True
			# print "ol"
			url = get_url(data)
			portflag = True
			ip, port = get_ip_port(url)

			if blacklist(port) or portflag:
				real_client.send("Enter username and password with a space between them\n")
				users = real_client.recv(1024)

				if not authenticated_user(users):
					real_client.send("Wrong Credentials!\nThis url is blocked!!\n$\n")
					real_client.close()
					print "Severing connection"
					continue

			if url in cache and  not modified(url):
				data = cache[url][0]
				gotData = True
				real_client.send(data)
				if(gotData):
					real_client.close()
				
			t1 = threading.Thread(target=self.connect_to_server, args=(real_client, ip, port, data,url))
			startThread = 1
			t1.start()

	def connect_to_server(self,real_client, ip, port, data,url):
		c = Client(ip, port, data)
		maxnum = 1024
		c.cnct(maxnum, real_client,url)
		real_client.close()
