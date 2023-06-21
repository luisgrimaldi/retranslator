import time
def saveError(response, cliente):
    txt = "Código de error " + str(response.status_code) + " " + response.reason + "\n"
    txt += "Response: \n" + response.content.decode() + "\n\n"
    txt += "Body: \n" + response.request.body

    fileName = "Mensajes/error " + cliente + " " +str(round(time.time()*1000)) + ".txt" 
    f = open(fileName, "a")
    f.write(txt)
    f.close()

def saveOK(response, cliente):
    ##txt = "Código de error " + str(response.status_code) + " " + response.reason + "\n"
    txt = "Response: \n" + response.content.decode() + "\n\n"
    txt += "Body: \n" + response.request.body

    fileName = "Mensajes/OK " + cliente + " " + str(round(time.time()*1000)) + ".txt" 
    f = open(fileName, "a")
    f.write(txt)
    f.close()

def saveExcept(text, cliente):
    fileName = "Mensajes/Exception " + cliente + " " + str(round(time.time()*1000)) + ".txt" 
    f = open(fileName, "a")
    f.write(text)
    f.close()
