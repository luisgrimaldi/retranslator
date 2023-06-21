import requests
import Exceptions as Ex
from datetime import datetime

def insertUnits(data):
    try:
        url="http://bft1.dogoit.com/ws_integration/service.php"
        headers={'Content-Type':'text/xml;charset=UTF-8', 'SOAPAction':'http://bft1.dogoit.com/ws_integration/service.php/insertUnits', 'Accept-Encoding':'gzip,deflate'}
        
        body1= """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:integrationCTTMX">
        <soapenv:Header/>
        <soapenv:Body>
        <urn:insertUnits soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">"""
        usuario = "<user xsi:type='xsd:string'>trpatlan</user>"
        password = "<pass xsi:type='xsd:string'>x0p0CXedPS</pass>"
        body2 = """<arrayOfUnits xsi:type="urn:items">
            <item xsi:type="urn:unit">"""
        placa = "<placa xsi:type='xsd:string'>"+data["asset"]+"</placa>"
        economico = "<economico xsi:type='xsd:string'>"+data["economico"]+"</economico>"
        timestamp = "<timestamp xsi:type='xsd:int'>"+str(int(datetime.now().timestamp()))+"</timestamp>"
        latitude = "<latitude xsi:type='xsd:float'>"+data["latitude"]+"</latitude>"
        longitude = "<longitude xsi:type='xsd:float'>"+data["longitude"]+"</longitude>"
        height = "<height xsi:type='xsd:int'>"+data["height"]+"</height>"
        odometer = "<odometer xsi:type='xsd:int'>"+data["odometer"]+"</odometer>"
        speed = "<speed xsi:type='xsd:int'>"+data["speed"]+"</speed>"
        course = "<course xsi:type='xsd:int'>"+data["course"]+"</course>"
        sats = "<sats xsi:type='xsd:int'>"+data["sats"]+"</sats>"
        event = "<event xsi:type='xsd:int'>0</event>"
        temp ="<temp xsi:type='xsd:float'>"+data["temp"]+"</temp>"
        unitType = "<unitType xsi:type='xsd:int'>"+data["unitType"]+"</unitType>"
        engine = "<engine xsi:type='xsd:int'>"+data["engine"]+"</engine>"
        body3 ="""</item>
        </arrayOfUnits>
        </urn:insertUnits>
        </soapenv:Body>
        </soapenv:Envelope>"""
        
        body = body1 + usuario + password + body2 + placa + economico + timestamp + latitude + longitude + height + odometer + speed + course + sats + event + temp + unitType + engine + body3
        response = requests.post(url, data=body, headers=headers)
        if response.status_code != 200:
            Ex.saveError(response, "BAFAR")
            #print(response.content.decode())
        else:
            Ex.saveOK(response, "BAFAR")
            #print(response.content.decode())
    except Exception as e:
        Ex.saveExcept("OS error: {0}".format(e), "BAFAR")
