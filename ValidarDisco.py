import psutil
import os
import threading
import time

# Tarea a ejecutarse cada determinado tiempo.
def timer():
	while True:
		disk_usage = psutil.disk_usage("/")
		if float(disk_usage.percent)<60.0:
			print("Aún queda espacio disponible. Se ha utilizado menos del 80%")
		else:
			print("Ya hay más del 80% de espacio utilizado. Se borrarán archivos de mensajes y Nohup.")
			dir = "Mensajes"
			for f in os.listdir(dir):
				#print(os.path.join(dir,f))
				os.remove(os.path.join(dir, f))
				f = open("nohup.out", "w")
				f.write("")
				f.close()
		time.sleep(21600)   # 6 hrs.
# Iniciar la ejecución en segundo plano.
t = threading.Thread(target=timer)
t.start()
