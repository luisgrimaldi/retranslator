import time
def saveError(response):
    nameFile = ""
    txt = "Código de error " + str(response.status_code) + " " + response.reason + "\n"
    txt += "Response: \n" + response.content.decode() + "\n\n"
    txt += "Body: \n" + response.request.body

    fileName = "error " + str(round(time.time()*1000)) + ".txt" 
    f = open(fileName, "a")
    f.write(txt)
    f.close()

def saveOK(response):
    nameFile = ""
    ##txt = "Código de error " + str(response.status_code) + " " + response.reason + "\n"
    txt = "Response: \n" + response.content.decode() + "\n\n"
    txt += "Body: \n" + response.request.body

    fileName = "OK " + str(round(time.time()*1000)) + ".txt" 
    f = open(fileName, "a")
    f.write(txt)
    f.close()