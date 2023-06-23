# -*- coding: utf-8 -*-

import threading
import socket
import Exceptions as Ex
import Retranslator as R

CONNECTION = (socket.gethostname(), 80)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((socket.gethostname(), 80))
server.listen(100)


def clientthread(conn):

	serialNumber = ""
	while True:
    
		try:
			#Recibe datos del cliente
			data = conn.recv(65495)
			if not data:
				break
			#print(data)#print("\n"+str(serialNumber)+ " package:    " + data.decode() + "\n\n")
			serialNumber = R.retranslate(data.decode(), serialNumber)
         
            
			# el paquete fue recibido con exito
			conn.send("OK".encode())
		except Exception as e:
			Ex.saveExcept("OS error: {0}".format(e), "SERVER")
	conn.close()

while True:

	print ("Listen {0} on {1}".format(*CONNECTION))
	sck, addr = server.accept()
	print ("Connected {0}:{1}".format(*addr))
	t = threading.Thread(target=clientthread, args=(sck,))
	t.daemon = True
	t.start()

#conn.close()
sck.close()
