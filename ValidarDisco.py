import psutil
import os

disk_usage = psutil.disk_usage("/")
if float(disk_usage.percent)<30.0:
	print("Aún queda espacio disponible. Se ha utilizado menos del 80%")
else:
	print("Ya hay más del 80% de espacio utilizado. Se borrarán archivos de mensajes y Nohup.")
	dir = "Mensajes"
	for f in os.listdir(dir):
		#print(os.path.join(dir,f))
		os.remove(os.path.join(dir, f))
		f = open("nohup.out", "w")
		f.write("nuevo")
		f.close()
