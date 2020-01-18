import socket
import threading
import signal


import sys
import time
from proxy_serv import *
accounts = []
request_url_time = {}
# from func1 import *



def modified(url):
	if url not in cache:
		return False
	else:
		s.send("GET /" + url + " HTTP/1.1\r\nIf-Modified-Since: " + cache[url][-1] + " \r\n\r\n")
	reply = s.recv(100000)
	# print "ok"
	if reply.find("200") < 0:
		return False
	else:
		return True

def to_cache(url):
	port1 = True
	flagx = 0
	if url not in request_url_time or port1:
		request_url_time[url] = [time.time()]
		# print url
	else:
		request_url_time[url].append(time.time())
		port1 = None
		if len(request_url_time[url]) > 3:
			request_url_time[url].pop(0)
			cache1 = False
			# print cache1
			# print "lol"
			if request_url_time[url][2] - request_url_time[url][0] <= 300 or not cache1:
				flagx = 1
				return True
	if not flagx:
		return False


def fill_users():
	with open('proxy/allowed_users.txt', 'r') as file:
		file_flag = None
		for line in file:
			line = line.split(' ')
			file_flag = True
			accounts.append([line[0], line[1]])
		if(file_flag):
			success = 1



def main():
	fill_users()
	# print accounts
	s = Server()
	s.listen(5)



if __name__== "__main__":
	main()



