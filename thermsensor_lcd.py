import time
from datetime import datetime
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "RbpiLocalApp.settings"
import django
django.setup()
from django.core.files import File
from  w1thermsensor import W1ThermSensor
import drivers
from picamera import PiCamera
from gpiozero import Button
from app.models import *

camera = PiCamera()
select_button = Button(19) #35
accept_button = Button(26) #37

sensor = W1ThermSensor()
display = drivers.Lcd()

predios = Predio.objects.all() #values_list('nombre', flat=True))
lanza = Lanza.objects.get(id=1)
predio_selected = None
pila_selected = None

def showPredios():
	global predio_selected
	i=0
	while 1:
		if accept_button.is_pressed:
			predio_selected = predios[i]
			print(predio_selected)
			break
		display.lcd_display_string("Elija predio:", 1)
		display.lcd_display_string(predios[i].nombre,2)
		if select_button.is_pressed:
			print(i)
			i+=1
			display.lcd_display_string(" "*16,2)
		if i==len(predios):
			i=0

def showPilas(predio):
	global pila_selected
	pilas = Pila.objects.filter(predio=predio.id)
	if not pilas:
		display.lcd_display_string("PREDIO SIN PILAS",1)
		display.lcd_display_string("REGISTRADAS X",2)
		time.sleep(2)
		return
	i=0
	while 1:
		if accept_button.is_pressed:
			pila_selected = pilas[i]
			print(pila_selected)
			break
		display.lcd_display_string("Elija pila:", 1)
		display.lcd_display_string(pilas[i].nombreID,2)
		if select_button.is_pressed:
			print(i)
			i+=1
			display.lcd_display_string(" "*16,2)
		if i==len(predios)-1:
			i=0

try:
	display.lcd_display_string("BIENVENIDO", 1)
	display.lcd_display_string("v. 1.0.1", 2)
	display.lcd_clear()
	while True:
		temp = sensor.get_temperature() #temp en celcius
		print("Temperatura en celcius", temp)
		time.sleep(2)
		showPredios()
		time.sleep(2)
		display.lcd_clear()
		showPilas(predio_selected)
		display.lcd_clear()
		print("OK")
		display.lcd_display_string(f"temp. {temp:.2f} {chr(223)}C", 1)
		display.lcd_display_string("humedad 57 %", 2)
		time.sleep(5)
		#TOMAR FOTO
		t = datetime.now().strftime("%H%M_%d%m%Y")
		pred = predio_selected.nombre.replace(" ", "_")
		path_photo = "/home/pi/Desktop/"
		name_photo = f"{pila_selected.nombreID}{pred}{t}.png"
		Cpath_photo = path_photo+name_photo
		camera.start_preview()
		camera.capture(Cpath_photo)
		camera.stop_preview()
		print("FOTO GUARDADA!!")
		#OBTENER POSICION
		print("fake position")
		#GUARDAR EN BD LOCAL
		medicion = Medicion(
			temperatura=int(temp),
			humedad=57,
#			foto=my_photo,
			lanza=lanza,
			pila=pila_selected
			)
		medicion.foto.save(name_photo, File(open(Cpath_photo,'rb')))
		print("objeto creado")
		medicion.save()
		print("objeto guardado en BD Local!!!")
		#ENVIAR POR REST A REMOTO (solo si hay interneT)
		#display.lcd_clear()
		#display.lcd_display_string("DATOS", 1)
		#display.lcd_display_string("GUARDADOS", 2)
		#time.sleep(10)
		#display.lcd_clear()
#time.sleep(1)
		#display.lcd_clear()
		display.lcd_clear()
except KeyboardInterrupt:
	print("Terminado!")
	display.lcd_clear()
