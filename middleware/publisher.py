import sys
import zmq
from threading import Thread
import random
import datetime
import os
import time

class publisher(Thread):

	def __init__(self, id, topic, flood):
		super().__init__()
		self.id = int(id)
		self.topic = topic
		self.flood = flood
		self.joined = True

	def run(self):
		print('starting publisher number ' + str(self.id))
		context = zmq.Context()
		pub = context.socket(zmq.PUB)
		print('Flood variable is ' + self.flood)
		if self.flood != True:
			print('Flooding Approach Enabled for Publisher')

			port = int(5558 + self.id + 4)

			#FIXME: Edit the binding to seek the appropriate IP 10.0.0.#
			#pub.bind("tcp://10.0.0." + str(self.id) + ":" + str(5558 + self.id))
			print("tcp://10.0.0.{ipid}:{portid}".format(ipid=self.id, portid=port))
			#pub.bind("tcp://10.0.0." + int(self.id) + ':' + port)

			pub.bind("tcp://10.0.0.6:{portid}".format(portid=port))
			#Working pub.bind("tcp://10.0.0.{ipid}:{portid}".format(ipid=self.id, portid=port))
			#pub.bind("tcp://10.0.0.{ipid}:{portid}".format(ipid=self.id, portid=(port)))
		else:
			print('Broker Approach Enabled for Publisher')
			pub.connect("tcp://10.0.0.1:5560")
		while self.joined:
			#select a stock
			stock_list = ["GOOG", "AAPL", "MSFT", "IBM", "AMD", "CLII", "EXO", "NFLX", "CME", "CKA"]
			index = random.randrange(1,10)
			#topic = stock_list[index]
			#generate a random price
			price = str(random.randrange(20, 60))
			#send topic + price to broker

			#Capturing system time
			#seconds = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
			#time = seconds
			time_started = (datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()
			pub.send_string("{topic} {price} {time_started}".format(topic=self.topic, price=price, time_started=time_started))
			time.sleep(1)

	def leave(self):
		self.joined = False
		print('pub leaving')


def main():
	id = sys.argv[1]
	topic = sys.argv[2]
	method = sys.argv[3]

	pub = publisher(id, topic, method)
	pub.start()
	#while True:
		#pub.start()
		#time.sleep(1)

if __name__=='__main__':
	main()