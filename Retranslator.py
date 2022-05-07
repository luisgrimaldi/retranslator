import RCService as RCS
import BAFARService as BS
import math



def retranslate(packages, serialNumber):
	validParams= {
    "pwr_ext":"battery",
	"accum_0":"battery", #LMU-300
	"io_239":"ignition", #Teltonika
	"ign":"ignition",	 #Suntech
	#"tr-status":"ignition", #Xeelectech LK210
	"odom": "odometer"   #Topflytech TLP1-SF
	}	

	data = {
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
	#[placa]
	serialNumbersRC={
		"customerName":"MIGUEL MARIO INZUNZA LUQUE",
		"customerId":"41013",
		"010182033":["35AB3D"],
		"352094089692658":["36AG9D"],
		"862522030189922":["30AB3D"],
		"1332012441":["71AB2D"]
	}
	#[placa, tipoUnidad, Economico]
	serialNumbersBAFAR={
		"010192001":["306EP8","1", "030"],
		"359857084519479":["896AF9", "1", "031"],
		"9172094393":["105EX1", "1", "032"],
		"359857084531268":["139AM9", "1", "033"],
		"869530045121395":["71AC1G","1", "034"],
		"869530041397205":["70AC1G", "1", "035"],
		"9172094470":["", "1", "037"],
		"359857084525708":["103XR5","2", "1996"],
		"865284045642240":["25UJ5W","2", "2014"],
		"865284045656521":["41UF6Z","2", "1914"],
		"359857084525815":["36UE7U","2", "1964"],
		"359857084029560":["45UC7X","2", "1983"],
		"865284045649955":["46UC7X","2", "1989"],
		"860112041825748":["951UP2","2", "1995"],
		"865284040021697":["952UP2","2", "1997"],
		"868899049001973":["580M", "6", ""]
	}

	packages = packages.replace(" ","")
	packages = packages.split("\n")
	serialNumberAux = ""
	if serialNumber:
		serialNumberAux = serialNumber
	
	for package in packages:
		if package[0:3] != "#D#":
			if package[0:3] == "#L#":
				serialNumberAux=package[3:len(package)-4]
			continue
				
		x = package[3:len(package)].split(";")

		if x[2] == "NA":
			continue

		data["altitude"]=x[8]
		#data["asset"]=x[] *NA
		#data["battery"]=x[] *find in Params
		#data["code"]=x[] *NA
		data["course"]=x[7]		
		#YYYY-MM-DDTHH:MM:SS
		#030122;195437
		data["date"]="20" + x[0][4:6] + "-" + x[0][2:4] + "-" + x[0][0:2] + "T" + x[1][0:2] + ":" + x[1][2:4] + ":" + x[1][4:6]
		#data["direction"]=x[] *See Wialon API for address
		#data["ignition"]=x[] *NA
		data["latitude"]=x[2]
		data["longitude"]=x[4]
		#data["odometer"]=x[] *NA
		data["serialNumber"]= serialNumberAux
		#data["shipment"]=x[] *NA
		data["speed"]=x[6]
		data["sats"]=x[9]
			
		params = x[len(x)-1].split(",")
		for p in params:
			param = p.split(":")
			if param[0] in validParams:
				data[validParams.get(param[0])]= param[2]
		#print(str(serialNumber))
		if serialNumberAux in serialNumbersRC:
			data["asset"] = serialNumbersRC.get(serialNumberAux)[0]
			data["customerId"]=serialNumbersRC.get("customerId")
			data["customerName"]=serialNumbersRC.get("customerName")
			#print("RC	"+str(data))
			token = RCS.getToken()
			if token:
				RCS.gpsAssetTracking(token, data)			
		elif serialNumberAux in serialNumbersBAFAR:
			data["asset"] = serialNumbersBAFAR.get(serialNumberAux)[0]
			data["unitType"] = serialNumbersBAFAR.get(serialNumberAux)[1]
			data["economico"] = serialNumbersBAFAR.get(serialNumberAux)[2]
			BS.insertUnits(data)		
			#print("BAFAR	"+str(data))

	return serialNumberAux

def convertCoordinates(type, coordinate, orientation):
	lCoordinate = ""
	lDegree = ""
	lMinutes = ""
	lSign = ""
	if type == "lat":
		lCoordinate = coordinate.split(".")
		if len(lCoordinate[0]) == 4:
			lDegree = int(lCoordinate[0][0:2])
			lMinutes = lCoordinate[0][2:4] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

		elif len(lCoordinate[0]) == 3:
			lDegree = int("0" + lCoordinate[0][0:1])
			lMinutes = lCoordinate[0][1:3] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

		elif len(lCoordinate[0]) == 2:
			lDegree = int("00")
			lMinutes = lCoordinate[0] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

	elif type == "lon":
		lCoordinate = coordinate.split(".")
		if len(lCoordinate[0]) == 5:
			lDegree = int(lCoordinate[0][0:3])
			lMinutes = lCoordinate[0][3:5] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes
			
		elif len(lCoordinate[0]) == 4:
			lDegree = int("0" + lCoordinate[0][0:2])
			lMinutes = lCoordinate[0][2:4] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

		elif len(lCoordinate[0]) == 3:
			lDegree = int("00" + lCoordinate[0][0:1])
			lMinutes = lCoordinate[0][1:3] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

		elif len(lCoordinate[0]) == 2:
			lDegree = int("000")
			lMinutes = lCoordinate[0] +"."+ lCoordinate[1]
			lMinutes = float(lMinutes)/60
			lCoordinate = lDegree + lMinutes

	if orientation == "S" or orientation == "W":
		lSign = "-"
			
	if len(str(lCoordinate).split(".")[1]) > 6:
		lCoordinate = "{:.6f}".format(lCoordinate)
	else:
		lCoordinate = str(lCoordinate)
	
	lCoordinate = lSign + lCoordinate

	return lCoordinate


#test data 

package = """#L#010192001;NA
#D#050522;181142;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;network_operator:3:bueno cell,access_name:3:CAT-M1,band_name:3:LTE BAND 4,imsi:3:334020032220933,iccid:3:8952020619390162987F
"""

package2 = """#L#865284045656521;NA
		#D#220422;231205;2034.6814;N;10024.2249;W;47;166;1809.0;12;NA;NA;NA;NA;NA;gnss_status:1:76,alarm:1:0,acc_x:2:0.2,acc_y:2:-0.1,acc_z:2:0.8,battery_percent:1:98,temp:1:34,front_light:2:1.8,pwr_int:2:4.0,solar_voltage:2:4.3,odom:1:25897815,status:1:1604,network_signal:1:100,acc_on:1:120,acc_off:1:3600,angle:1:20,distance:1:0,heart:1:0,settings_status:1:12500
#D#220422;231210;2034.6535;N;10024.2345;W;48;207;1805.0;12;NA;NA;NA;NA;NA;gnss_status:1:76,alarm:1:0,acc_x:2:0.0,acc_y:2:-0.1,acc_z:2:0.9,battery_percent:1:97,temp:1:34,front_light:2:1.8,pwr_int:2:4.0,solar_voltage:2:5.5,odom:1:25897870,status:1:1612,network_signal:1:100,acc_on:1:120,acc_off:1:3600,angle:1:20,distance:1:0,heart:1:0,settings_status:1:12500
#D#220422;231215;2034.6246;N;10024.2656;W;43;241;1803.0;12;NA;NA;NA;NA;NA;gnss_status:1:76,alarm:1:0,acc_x:2:0.0,acc_y:2:-0.1,acc_z:2:0.9,battery_percent:1:98,temp:1:34,front_light:2:1.8,pwr_int:2:4.0,solar_voltage:2:5.5,odom:1:25897947,status:1:1612,network_signal:1:100,acc_on:1:120,acc_off:1:3600,angle:1:20,distance:1:0,heart:1:0,settings_status:1:12500
#D#220422;231223;2034.6129;N;10024.3159;W;46;265;1807.0;10;NA;NA;NA;NA;NA;gnss_status:1:74,alarm:1:0,acc_x:2:0.0,acc_y:2:-0.2,acc_z:2:1.0,battery_percent:1:98,temp:1:34,front_light:2:1.8,pwr_int:2:4.0,solar_voltage:2:5.5,odom:1:25898038,status:1:1612,network_signal:1:100,acc_on:1:120,acc_off:1:3600,angle:1:20,distance:1:0,heart:1:0,settings_status:1:12500
"""

if __name__ == "__main__":
	#serialNumber = ""
	#serialNumber = retranslate(package, serialNumber)
	#serialNumber = ""
	#serialNumber = retranslate(package2, serialNumber)
	print(convertCoordinates("lat", "5544.6025", "N"))
	print(convertCoordinates("lon", "03739.6834", "E"))