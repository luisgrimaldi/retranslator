import requests
import Exceptions as Ex



def getToken():
	url= "http://gps.rcontrol.com.mx/Tracking/wcf/RCService.svc"
	headers={'Content-Type':'text/xml;charset=UTF-8', 'SOAPAction':'http://tempuri.org/IRCService/GetUserToken', 'Accept':'application/xml'}

	body="""<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:tem='http://tempuri.org/'>
	<soapenv:Header>
	</soapenv:Header>
	<soapenv:Body>
		<tem:GetUserToken>
			<tem:userId>ws_avl_saverenlinea</tem:userId>
			<tem:password>tNfX$448tSfA*7</tem:password>
		</tem:GetUserToken>
	</soapenv:Body>
	</soapenv:Envelope>"""
	try:
		response = requests.post(url, data=body, headers=headers)
		if response.status_code != 200:
			Ex.saveError(response)
			return ""
		else:
			token = response.content.decode("utf-8").split('token>')
			token = token[1].split('<')
			token = token[0]
			return token
	except Exception as e:
		Ex.saveExcept("OS error: {0}".format(e))
		return ""

def gpsAssetTracking(token, data):

	url="http://gps.rcontrol.com.mx/Tracking/wcf/RCService.svc"
	headers={'Content-Type':'text/xml;charset=UTF-8', 'SOAPAction':'http://tempuri.org/IRCService/GPSAssetTracking', 'Accept':'gzip,deflate'}
	
	body1="""<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:tem='http://tempuri.org/' xmlns:iron='http://schemas.datacontract.org/2004/07/IronTracking'>
 	<soapenv:Header/>
	<soapenv:Body>
	<tem:GPSAssetTracking>"""

	try:

		token= "<tem:token>" + token + "</tem:token>" 
		body2="""<tem:events> 
			<iron:Event>"""	
		altitude= "<iron:altitude>"+ data["altitude"] + "</iron:altitude>"
		asset="<iron:asset>" + data["asset"] + "</iron:asset>" 
		battery= "<iron:battery>" + data["battery"] + "</iron:battery>" 
		code= "<iron:code>" + data["code"] + "</iron:code>" 
		course= "<iron:course>" + data["course"] + "</iron:course>" 
		customer1= "<iron:customer>" 
		customer2= "<iron:id>" + data["customerId"] + "</iron:id>" 
		customer3= "<iron:name>" + data["customerName"] + "</iron:name>"
		customer4= "</iron:customer>"
		date= "<iron:date>" + data["date"] + "</iron:date>"
		direction= "<iron:direction>" + data["direction"] + "</iron:direction>"
		ignition= "<iron:ignition>" + data["ignition"] + "</iron:ignition>"
		latitude= "<iron:latitude>" + data["latitude"] + "</iron:latitude>"
		longitude= "<iron:longitude>" + data["longitude"] + "</iron:longitude>"
		odometer= "<iron:odometer>" + data["odometer"] + "</iron:odometer>"
		serialNumber= "<iron:serialNumber>" + data["serialNumber"] + "</iron:serialNumber>"
		shipment= "<iron:shipment>" + data["shipment"] + "</iron:shipment>"
		speed= "<iron:speed>" + data["speed"] + "</iron:speed>"
		body3= """</iron:Event>
			</tem:events>
			</tem:GPSAssetTracking>
			</soapenv:Body>
			</soapenv:Envelope>"""

		body= body1 + token + body2 + altitude + asset + battery + code + course + customer1 + customer2 + customer3 + customer4 + date + direction + ignition + latitude + longitude + odometer + serialNumber + shipment + speed + body3
		
		response = requests.post(url, data=body, headers=headers)
		if response.status_code != 200:
			#print(response.content.decode())
			Ex.saveError(response)
		#else:
			#print(response.content.decode())
			#Ex.saveOK(response)
	
	except Exception as e:
		Ex.saveExcept("OS error: {0}".format(e))

	#print (response)
	#return body