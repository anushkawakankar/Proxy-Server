import socket			 
import sys
porrt = None
binded = None
soc = socket.socket()		 
print "Socket successfully created"

port = int(sys.argv[1])

soc.bind(('', port))
porrt=True
print "Binded: %s" %(port)
binded=True
soc.listen(5)
print "Listening..."	

while True and binded: 
	c, addr = soc.accept()	 
	print 'Connection request:', addr
	c.send('Connection established!')
	c.close()