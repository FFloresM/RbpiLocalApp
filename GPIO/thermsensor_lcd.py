import time
import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'RbpiLocalApp.settings'
from  w1thermsensor import W1ThermSensor
import drivers
from gpiozero import Button
from .app.models import Pila


button = Button(21)

sensor = W1ThermSensor()
display = drivers.Lcd()

a = Pila.objects.get(id=1)

try:
	display.lcd_display_string("BIENVENIDO", 1)
	display.lcd_display_string("v. 1.0.1", 2)
	time.sleep(2)
	display.lcd_clear()
	display.lcd_display_string(f"Pila {a.nombreID}", 1)
	display.lcd_clear()
	while True:
		if button.is_pressed:
			display.lcd_display_string("BOTON!!",1)
		temp = sensor.get_temperature() #temp en celcius
		#print("Temperatura en celcius", temp)
		display.lcd_display_string("Temperatura pila", 1)
		display.lcd_display_string(f"{temp:.2f} {chr(223)}C", 2)
		#time.sleep(1)
		#display.lcd_clear()

except KeyboardInterrupt:
	print("Terminado!")
	display.lcd_clear()
