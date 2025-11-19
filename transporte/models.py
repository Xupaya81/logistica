from django.db import models

# ------------------------------------------------
# CHOICES
# ------------------------------------------------

TIPO_TRANSPORTE = [
    ('TERRESTRE', 'Transporte Terrestre'),
    ('AEREO', 'Transporte Aéreo'),
]

ESTADO_DESPACHO = [
    ('PENDIENTE', 'Pendiente'),
    ('EN_RUTA', 'En Ruta'),
    ('ENTREGADO', 'Entregado'),
]


# ------------------------------------------------
# MODELOS PRINCIPALES
# ------------------------------------------------

class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad_kg = models.IntegerField()
    tipo_transporte = models.CharField(max_length=15, choices=TIPO_TRANSPORTE, default='TERRESTRE')

    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"


class Aeronave(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=50)
    capacidad_kg = models.IntegerField()

    def __str__(self):
        return f"{self.codigo} - {self.modelo}"


class Conductor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    licencia = models.CharField(max_length=20, unique=True)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Piloto(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    certificacion = models.CharField(max_length=100)
    vigente = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class Carga(models.Model):
    descripcion = models.CharField(max_length=200)
    peso_kg = models.IntegerField()
    tipo = models.CharField(max_length=50)
    valor = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cargas")

    def __str__(self):
        return f"{self.descripcion} - {self.peso_kg} kg"


class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    tipo_transporte = models.CharField(max_length=15, choices=TIPO_TRANSPORTE)
    distancia_km = models.IntegerField()

    def __str__(self):
        return f"{self.origen} → {self.destino}"


class Despacho(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True, blank=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    piloto = models.ForeignKey(Piloto, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_DESPACHO, default='PENDIENTE')

    def __str__(self):
        return self.codigo
