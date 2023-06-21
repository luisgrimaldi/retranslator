# -*- coding: utf-8 -*-

import threading
import socket
import Retranslator as R

CONNECTION = (socket.gethostname(), 80)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((socket.gethostname(), 80))
server.listen(15)


def clientthread(conn):

    serialNumber = ""
    while True:
        #Recibe datos del cliente
        data = conn.recv(65495)
        if not data:
            break
        print("\n"+str(serialNumber)+ " package:    " + data.decode() + "\n\n")
        #print(data)
        #serialNumber = R.retranslate(data.decode(), serialNumber)
         
            
        # el paquete fue recibido con exito
        conn.send("OK".encode())
        #test
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
