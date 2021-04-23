import time
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "RbpiLocalApp.settings"
import django
django.setup()
from  w1thermsensor import W1ThermSensor
import drivers
from gpiozero import Button
from app.models import *

select_button = Button(19) #35
accept_button = Button(26) #37

sensor = W1ThermSensor()
display = drivers.Lcd()

predios = list(Predio.objects.values_list('nombre', flat=True))
predio_selected = None

def showPredios():
	i=0
	while 1:
		display.lcd_clear()
		display.lcd_display_string("Seleccione predio:", 1)
		display.lcd_display_string(predios[i],2)
		if i==len(predios)-1:
			i=0
		if accept_button.is_pressed:
			predio_selected = predios[i]
			print(predio_selected)
			break
		select_button.wait_for_press()
		i+=1

try:
	display.lcd_clear()
	while True:
		#if select_button.is_pressed:
		#	display.lcd_display_string("BOTON 1!!",1)
		temp = sensor.get_temperature() #temp en celcius
		print("Temperatura en celcius", temp)
		display.lcd_display_string("BIENVENIDO", 1)
		display.lcd_display_string("v. 1.0.1", 2)
		time.sleep(1)
		showPredios()
		time.sleep(5)
		display.lcd_clear()
		#display.lcd_display_string(f"temp. 11.4 {chr(223)}C", 1)
		#display.lcd_display_string(f"{temp:.2f} {chr(223)}C", 2)
		#display.lcd_display_string("humedad 57 %", 2)
		#time.sleep(10)
		#display.lcd_clear()
		#display.lcd_display_string("DATOS", 1)
		#display.lcd_display_string("GUARDADOS", 2)
		#time.sleep(10)
		#display.lcd_clear()
#time.sleep(1)
		#display.lcd_clear()

except KeyboardInterrupt:
	print("Terminado!")
	display.lcd_clear()
