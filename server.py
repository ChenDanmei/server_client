# server

import zmq
import sys
import threading
import time
from random import randint, random, randrange

seuil = 2000
clients = [0, 0]
requst_total = 0

lock = threading.Lock()

class ServerTask(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        numClient = 2
        
        #broadcast to client0, ip = 10.195.96.129
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.sndhwm = 1100000
        publisher.connect("tcp://10.195.96.129:5556")

        #broadcast to client1, ip = 10.195.96.98
        context = zmq.Context()
        publisher1 = context.socket(zmq.PUB)
        publisher1.sndhwm = 1100000
        publisher1.connect("tcp://10.195.96.98:5556")
                
        while True:
            lock.acquire()
            try:
                #fetch data from shared object
                global seuil
                global clients
                global requst_total
                source = seuil - requst_total
                #publisher.send_string("%i " % (source))
                print("capacite: %s" % (source))
            finally:
                lock.release()
                
            if source >=0:
                publisher.send_string("%i " % (clients[0]))
                publisher1.send_string("%i " % (clients[1]))
            else:
                mss = clients[0] + source / numClient
                mss1 = clients[1] + source / numClient
                publisher.send_string("%i " % (mss))
                publisher1.send_string("%i " % (mss1))

                        
            time.sleep(1)

        socket.close()
        context.term()


class ServerUpadate(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.bind("tcp://*:5555")
        socket.setsockopt(zmq.SUBSCRIBE, b'')
        while True:
            string = socket.recv_string()
            identite, message = string.split()
            print("Received request from client%s: %s" % (identite, message))
            id = int(identite)
            requst = int(message)
            lock.acquire()
            try:
                #fetch data from shared object
                global clients
                clients[id] = requst
                global requst_total
                requst_total = sum(clients)
            finally:
                lock.release()
        socket.close()
        context.term()


def main():
    server = ServerTask()
    server.start()
    update = ServerUpadate()
    update.start()
    server.join()


if __name__ == "__main__":
    main()
