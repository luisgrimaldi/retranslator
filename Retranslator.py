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
			BS.insertUnits(data)		
			#print("BAFAR	"+str(data))

	return serialNumberAux


#test data 

package = """#L#352094089692658;NA
#D#200422;085200;2034.6566;N;10019.6076;W;0;0;2039.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.321,io_66:1:12321,pwr_int:2:4.129,io_67:1:4129
#D#200422;092200;2034.6566;N;10019.6076;W;0;0;2035.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.322,io_66:1:12322,pwr_int:2:4.128,io_67:1:4128
#D#200422;095200;2034.6566;N;10019.6076;W;0;0;2026.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.322,io_66:1:12322,pwr_int:2:4.128,io_67:1:4128
#D#200422;102200;2034.6566;N;10019.6076;W;0;0;2028.0;11;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.322,io_66:1:12322,pwr_int:2:4.128,io_67:1:4128
#D#200422;105200;2034.6566;N;10019.6076;W;0;0;2026.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.313,io_66:1:12313,pwr_int:2:4.126,io_67:1:4126
#D#200422;112200;2034.6566;N;10019.6076;W;0;0;2029.0;10;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.313,io_66:1:12313,pwr_int:2:4.126,io_67:1:4126
#D#200422;115200;2034.6566;N;10019.6076;W;0;0;2029.0;10;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.313,io_66:1:12313,pwr_int:2:4.126,io_67:1:4126
#D#200422;122200;2034.6566;N;10019.6076;W;0;0;2027.0;9;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.313,io_66:1:12313,pwr_int:2:4.126,io_67:1:4126
#D#200422;125200;2034.6566;N;10019.6076;W;0;0;2028.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.313,io_66:1:12313,pwr_int:2:4.126,io_67:1:4126
#D#200422;132200;2034.6566;N;10019.6076;W;0;0;2027.0;8;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.312,io_66:1:12312,pwr_int:2:4.125,io_67:1:4125
"""

package2 = """#L#010192001;NA
#D#200422;135200;2034.6566;N;10019.6076;W;0;0;2027.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.303,io_66:1:12303,pwr_int:2:4.125,io_67:1:4125
#D#200422;142200;2034.6534;N;10019.6078;W;0;0;2035.0;11;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.303,io_66:1:12303,pwr_int:2:4.125,io_67:1:4125
#D#200422;145200;2034.6534;N;10019.6078;W;0;0;2038.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.303,io_66:1:12303,pwr_int:2:4.125,io_67:1:4125
#D#200422;152200;2034.6534;N;10019.6078;W;0;0;2048.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.303,io_66:1:12303,pwr_int:2:4.123,io_67:1:4123
#D#200422;155200;2034.6534;N;10019.6078;W;0;0;2041.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.311,io_66:1:12311,pwr_int:2:4.123,io_67:1:4123
#D#200422;160914;2034.6534;N;10019.6078;W;0;0;2039.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.303,io_66:1:12303,pwr_int:2:4.123,io_67:1:4123
#D#200422;163914;2034.6534;N;10019.6078;W;0;0;2035.0;12;NA;NA;NA;NA;NA;prior:1:0,event_io_id:1:0,total_io:1:4,io_179:1:0,io_239:1:0,pwr_ext:2:12.312,io_66:1:12312,pwr_int:2:4.122,io_67:1:4122
"""

if __name__ == "__main__":
	serialNumber = ""
	serialNumber = retranslate(package, serialNumber)
	serialNumber = retranslate(package2, serialNumber)