import RCService as RCS
import BAFARService as BS



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
		"010182033":["35ABD"],
		"352094089692658":["36AG9D"],
		"862522030189922":["30AB3D"],
		"1332012441":["71AB2D"]
	}
	#[placa, tipoUnidad]
	serialNumbersBAFAR={
		"010192001":["306EP8","TR"],
		"359857084519479":["896AF9", "TR"],
		"9172094393":["105EX1", "TR"],
		"359857084531268":["139AM9", "TR"],
		"869530045121395":["71AC1G","TR"],
		"869530041397205":["70AC1G", "TR"],
		"9172094470":["NA", "TR"],
		"359857084525708":["103XR5","CA"],
		"865284045642240":["25UJ5W","CA"],
		"865284045656521":["41UF6Z","CA"],
		"359857084525815":["36UE7U","CA"],
		"359857084029560":["45UC7X","CA"],
		"865284045649955":["46UC7X","CA"],
		"860112041825748":["951UP2","CA"],
		"865284040021697":["952UP2","CA"],
		"868899049001973":["580M", "ND"]
	}

	packages = packages.replace(" ","")
	packages = packages.split("\n")
	serialNumberAux = ""
	if serialNumber:
		serialNumberAux = serialNumber
	
	for package in packages:
		if package[0:3] != "#D#":
			if package[0:3] == "#L#":
				serialNumberAux=package[3:len(package)-3]
			continue
				
		x = package[3:len(package)].split(";")
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
		#print(str(data))#print(str(serialNumber))
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
			BS.insertUnits(data)		
			#print("BAFAR	"+str(data))

	return serialNumberAux


#test data 

package = """#L#352094089692658;NA
#D#230422;000124;2034.6419;N;10019.6108;W;0;0;2030.0;10;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.498,io_66:1:12498,pwr_int:2:4.023,io_67:1:4023
"""

package2 = """#L#865284045656521;NA
#D#220422;231205;2034.6814;N;10024.2249;W;47;166;1809.0;12;NA;NA;NA;NA;NA;gnss_status:1:76,alarm:1:0,acc_x:2:0.2,acc_y:2:-0.1,acc_z:2:0.8,battery_percent:1:98,temp:1:34,front_light:2:1.8,pwr_int:2:4.0,solar_voltage:2:4.3,odom:1:25897815,status:1:1604,network_signal:1:100,acc_on:1:120,acc_off:1:3600,angle:1:20,distance:1:0,heart:1:0,settings_status:1:12500
"""

if __name__ == "__main__":
	serialNumber = ""
	serialNumber = retranslate(package2, serialNumber)
	#serialNumber = ""
	#serialNumber = retranslate(package2, serialNumber)