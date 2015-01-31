#!/usr/bin/env python
# coding:utf-8

__version__ = '0.0.1.1'
#
import sys
import random
import ssl
import socket
import sys
import httplib
import Queue
import threading

socket.setdefaulttimeout(30)

f = open('iprange-2.txt')
lines = f.readlines()
f.close()

q = Queue.Queue()
goodip=[]
def get_rand_ip():
	i = random.randint(0,len(lines)-1)
	j = str(random.randint(0, 255))
	return lines[i].strip() + '.' + j

def ping(ip):
	conn = httplib.HTTPConnection(ip)
	try:
		conn.request("HEAD","/")
		res = conn.getresponse()
		if res.status == 200 and res.getheader("server") == "gws":
			conn2 = httplib.HTTPSConnection(ip)
			conn2.request("HEAD","/")
			res = conn2.getresponse()
			if res.status == 200:
				print ip
				goodip.extend([ip])
				return 0
	except Exception, e:
		pass
	return -1

class PingThread(threading.Thread):
	""" Threading Ping """
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			ip = self.queue.get()
			ping(ip)
			self.queue.task_done()

def main():
	num_threads = 20
	num_ips = 100
	print "tesing 100 random ip addr with 20 threads. good ip addrs are:"
	for i in range(num_threads):
		t = PingThread(q)
		t.setDaemon(True)
		t.start()

	for x in range(num_ips):
		ip = get_rand_ip()
		q.put(ip)
	
	q.join()
	print 'tested good ip', len(goodip) 
	print '|'.join(goodip)
if __name__ == "__main__":
	main()