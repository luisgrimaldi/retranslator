import requests
import Exceptions as Ex
import json

def sendPositions(data):

	url="https://external.driv.in/api/external/v2/positions"
	headers={'X-API-Key': '03005362-d358-4d2b-823f-0acce16d2401', 'Content-Type': 'application/json'}
	positions= { "positions":[ data ] }
	print(positions)
	try:

		response = requests.post(url, data=json.dumps(data), headers=headers)
		if response.status_code != 201:
			#print(response.content.decode())
			Ex.saveError(response, "NUBUS")
		else:
			#print(response.content.decode())
			Ex.saveOK(response, "NUBUS")
	
	except Exception as e:
		Ex.saveExcept("OS error: {0}".format(e), "NUBUS")

	#print (response)
	#return body
if __name__ == "__main__":
  testData = {
		"device_number": 358480080906508,
		"vehicle_code": "41-AT-9P",
		"lat":2443.5793,
		"lng":10727.1027,
		#"accuracy":None,
		#"speed":None,
		#"battery_level":None,
		#"heading":None,
		"timestamp":1687127294000,
		#"acceleration":None,
		"temperature":{
			"temp1":42.2
		}
   }
  sendPositions(testData)
