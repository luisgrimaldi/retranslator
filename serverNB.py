# -*- coding: utf-8 -*-

import threading
import socket
import Exceptions as Ex
import Retranslator as R
import NUBUSService as NS
import math
from datetime import datetime

CONNECTION = (socket.gethostname(), 81)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((socket.gethostname(), 81))
server.listen(15)


def clientthread(conn):

	validParams= {
		"pwr_ext":"battery",
		"accum_0":"battery", #LMU-300
		"io_239":"ignition", #Teltonika
		"ign":"ignition",	 #Suntech
		#"tr-status":"ignition", #Xeelectech LK210
		"odom": "odometer",   #Topflytech TLP1-SF
		"temperature": "temperature"
	}

	datajson= {
		"altitude": "",
		"asset": "",
		"battery":"",
		"code":"",
		"course":"",
		"customerId":"",
		"customerName":"",
		"date":"",
		"direction":"",
		"ignition":"",
		"latitude":"",
		"longitude":"",
		"odometer":"",
		"serialNumber":"",
		"shipment":"",
		"speed":"",
		"sats":"",
		"unitType":"",
		"economico":"",
		"height":"",
		"temp":"",
		"engine":""
	}

	dataNubus = {
		"device_number": "",
		"vehicle_code": "",
		"lat":"",
		"lng":"",
		#"accuracy":None,
		#"speed":None,
		#"battery_level":None,
		#"heading":None,
		"timestamp":"",
		#"acceleration":None,
		"temperature":{
			"Temp1":""
		}
	}

	#[placa]
	serialNumberNubus={
		"358480080906508":["41AT9P"],
		"865284040201836":["03AT5R"]
	}

	while True:
 
		try:
     
			#Recibe datos del cliente
			data = conn.recv(65495)
			if not data:
				break
			#print("\n"+str(serialNumber)+ " package:    " + data.decode() + "\n\n")
        
			packages = data.decode()
        
			packages = packages.replace(" ","")
			packages = packages.split("\n")
        
			for package in packages:
				print(package)
				if package[0:3] != "#D#":
					if package[0:3] == "#L#":
						serialNumberAux=package[3:len(package)-4]
					continue
				x = package[3:len(package)].split(";")

				if x[2] == "NA":
					params = x[len(x)-1].split(",")
					for p in params:
						param = p.split(":")
						if param[0] in validParams:
							datajson[validParams.get(param[0])]= param[2]
				else:

					datajson["altitude"]=x[8]
					datajson["course"]=x[7]
					datajson["date"]="20" + x[0][4:6] + "-" + x[0][2:4] + "-" + x[0][0:2] + "T" + x[1][0:2] + ":" + x[1][2:4] + ":" + x[1][4:6]
					datajson["latitude"]=x[2]
					datajson["longitude"]=x[4]
					datajson["serialNumber"]= serialNumberAux
					datajson["speed"]=x[6]
					datajson["sats"]=x[9]
			
					params = x[len(x)-1].split(",")
					for p in params:
						param = p.split(":")
						if param[0] in validParams:
							datajson[validParams.get(param[0])]= param[2]
					if serialNumberAux in serialNumberNubus:
						dataNubus["device_number"] = serialNumberNubus.get(serialNumberAux)[0]
						dataNubus["vehicle_code"] = serialNumberNubus.get(serialNumberAux)[0]
						dataNubus["lat"] = float(R.convertCoordinates("lat",x[2], x[3]))
						dataNubus["lng"] = float(R.convertCoordinates("lon",x[4], x[5]))
						dataNubus["timestamp"] = int(R.dateToTimestamp(datajson["date"]))
						if datajson["temperature"]:
							dataNubus["temperature"]["Temp1"] = float(datajson["temperature"])
							#print("NUBUS	" + str(dataNubus))
							NS.sendPositions(dataNubus)
							dataNubus = {
								"device_number": "",
								"vehicle_code": "",
								"lat":"",
								"lng":"",
								#"accuracy":None,
								#"speed":None,
								#"battery_level":None,
								#"heading":None,
								"timestamp":"",
								#"acceleration":None,
								"temperature":{
									"Temp1":""
								}
							}

        		# el paquete fue recibido con exito
			conn.send("OK".encode())
        		#test

		except Exception as e:
			Ex.saveExcept("OS error: {0}".format(e), "SERVER_NB")
		
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
