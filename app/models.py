from django.db import models

class Cliente(models.Model):
    """ Empresa o agricultor que compra la lanza"""
    #id automatico con autoincremento
    nombre = models.CharField(max_length=200, default="")
    rut = models.CharField(max_length=9)
    direccion = models.CharField(max_length=200, default="")
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, default="")
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)

    def __str__(self):
        if self.nombre:
            return self.nombre
        return self.rut

    class Meta:
        ordering = ('nombre', )

class Lanza(models.Model):
    """Instrumento de medición"""
    codigo = models.CharField(max_length=100, unique=True, null=False)
    numero_serie = models.CharField("numero de serie", max_length=100, unique=True, null=False)
    modelo = models.CharField(max_length=20, default="")
    

    def __str__(self):
        return self.codigo

class Pila(models.Model):
    """Pila"""
    nombreID = models.CharField(max_length=10, default=None)
    predio = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField("fecha de creación", auto_now_add=True)
    estado = models.CharField(max_length=50)
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
    	return self.nombreID

    class Meta:
        ordering = ('cliente', )

class Medicion(models.Model):
    """Datos que son medidos por la lanza"""
    fecha_creacion = models.DateTimeField("fecha de creacion", auto_now_add=True)
    temperatura = models.IntegerField(default=0)
    humedad = models.IntegerField(null=True)
    foto = models.ImageField(upload_to='Fotos', null=True, blank=True) #crear folder Fotos
    posicion = models.CharField(max_length=20, null=True) #solo para prubas
    lanza = models.ForeignKey('Lanza', on_delete=models.DO_NOTHING)
    pila = models.ForeignKey('Pila', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Mediciones'
        ordering = ('lanza', )

class MateriaPrima(models.Model):
    """Materias primas utilizadas en el compost"""
    nombre = models.CharField(max_length=100, null=False)
    cantidad = models.IntegerField(null=False)
    unidad_medida = models.CharField(max_length=10, null=True)
    pila = models.ForeignKey('Pila', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Materias Primas'
        ordering = ('nombre', )
