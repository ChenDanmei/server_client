import zmq
import sys
import threading
import time
from random import randint, random, randrange

context = zmq.Context()


class ClientTask(threading.Thread):

  def __init__(self, id):
	  self.id = id
		threading.Thread.__init__(self)

	def run(self):
		print("Connecting to hello world server....")
		socket = context.socket(zmq.PUB)
		socket.sndhwm = 1100000
    
    #ip of server = 10.195.96.173
		socket.connect("tcp://10.195.96.173:5555")
		identite = 0

		while True:

			time.sleep(2)
			power = randrange(0, 2000)

			socket.send_string("%i %i" % (identite, power))
			print("Sending request from client0 : %s" % (power))


		socket.close()
		context.term()


class ClientUpadate(threading.Thread):


	def __init__(self, id):
        	self.id = id
        	threading.Thread.__init__(self)

	def run(self):
		context = zmq.Context()
		subscriber = context.socket(zmq.SUB)
		subscriber.bind('tcp://*:5556')
		subscriber.setsockopt(zmq.SUBSCRIBE, b'')

		while True:
			message = subscriber.recv()
			print("Received reply %s " % (message))


		socket.close()
		context.term()


def main():
	server = ClientTask(1)
	server.start()
	update = ClientUpadate(1)
	update.start()
	server.join()


if __name__ == "__main__":
	main()

