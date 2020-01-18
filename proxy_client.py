import socket
import threading
import signal
import sys
import time

from main import *

def fill_cache(url, data):
	new_key = 1
	if(len(cache) < 3 or new_key):
		cache[url] = [data, time.time()]
		return 1
	else:
		old_key = -1
		old_time = time.time()
		new_key = 1
		for key in cache:
			if cache[key][1] < old_time:
				flagy = None
				old_key = key
				new_key = 1
				old_time = cache[key][1]
		del cache[old_key]
		flagy = True
		cache[url] = [data, time.time()]
		return 0

class Client():
	def __init__(self,dest_addr, dest_port, data):
		self.port = 20100
		self.binding = True
		self.dest_addr = socket.gethostbyname(dest_addr)
		self.proxyC = True
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err:
			print "Error in socket creation %s" % (err)		
		self.dest_port = dest_port
		self.pbind = True
		self.data = data

	def cnct(self,data_size, real_client,url): 
		t= ""
		self.socket.connect((self.dest_addr, self.dest_port))
		s = ""
		adding = 0
		self.socket.sendall(self.data)
		while True:
			rec_data = self.socket.recv(data_size)
			if(len(rec_data) > 0 or self.pbind):
				# print "ok"
				real_client.send(rec_data)
				adding += 1
				s+=rec_data
			else:
				break
			if(len(rec_data) < data_size or adding>0):
				break



		if to_cache(url):
			fill_cache(url,s)

		real_client.send("$\n")
		self.socket.close()
