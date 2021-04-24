from gpiozero import Button

amarillo = Button(26)
rojo = Button(19)

while True:
	if amarillo.is_pressed:
		print("AMARILLO")
	elif rojo.is_pressed:
		print("ROJO")
	else:
		print("----------------")
