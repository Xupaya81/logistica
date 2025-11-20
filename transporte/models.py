from django.db import models

# ------------------------------------------------
# CHOICES (Opciones para campos de selección)
# ------------------------------------------------

# Opciones para el tipo de transporte
TIPO_TRANSPORTE = [
    ('TERRESTRE', 'Transporte Terrestre'),
    ('AEREO', 'Transporte Aéreo'),
]

# Opciones para el estado del despacho
ESTADO_DESPACHO = [
    ('PENDIENTE', 'Pendiente'),
    ('EN_RUTA', 'En Ruta'),
    ('ENTREGADO', 'Entregado'),
    ('CANCELADO', 'Cancelado'),
]

# ------------------------------------------------
# MODELOS PRINCIPALES
# ------------------------------------------------


class Vehiculo(models.Model):
    """
    Modelo que representa un vehículo de transporte terrestre.
    """
    patente = models.CharField(max_length=10, unique=True)  # Identificador único del vehículo
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad_kg = models.IntegerField()  # Capacidad de carga en kilogramos
    tipo_transporte = models.CharField(max_length=15, choices=TIPO_TRANSPORTE, default='TERRESTRE')

    def __str__(self):
        """Retorna una representación legible del vehículo."""
        return f"{self.patente} - {self.marca} {self.modelo}"


class Aeronave(models.Model):
    """
    Modelo que representa una aeronave de transporte aéreo.
    """
    codigo = models.CharField(max_length=20, unique=True)  # Código de identificación de la aeronave
    modelo = models.CharField(max_length=50)
    capacidad_kg = models.IntegerField()  # Capacidad de carga en kilogramos

    def __str__(self):
        """Retorna una representación legible de la aeronave."""
        return f"{self.codigo} - {self.modelo}"


class Conductor(models.Model):
    """
    Modelo que representa un conductor de vehículos terrestres.
    """
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    licencia = models.CharField(max_length=20, unique=True)  # Número de licencia de conducir
    vigente = models.BooleanField(default=True)  # Indica si el conductor está activo

    def __str__(self):
        """Retorna el nombre completo del conductor."""
        return f"{self.nombre} {self.apellido}"


class Piloto(models.Model):
    """
    Modelo que representa un piloto de aeronaves.
    """
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    certificacion = models.CharField(max_length=100)  # Certificación o licencia de vuelo
    vigente = models.BooleanField(default=True)  # Indica si el piloto está activo

    def __str__(self):
        """Retorna el nombre completo del piloto."""
        return f"{self.nombre} {self.apellido}"


class Cliente(models.Model):
    """
    Modelo que representa un cliente que solicita servicios de transporte.
    """
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, unique=True)  # Identificador tributario
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)  # Indica si el cliente está activo en el sistema

    def __str__(self):
        """Retorna el nombre del cliente."""
        return self.nombre


class Carga(models.Model):
    """
    Modelo que representa la carga a transportar.
    """
    descripcion = models.CharField(max_length=200)
    peso_kg = models.IntegerField()
    tipo = models.CharField(max_length=50)  # Tipo de carga (ej. frágil, general)
    valor = models.IntegerField()  # Valor monetario declarado de la carga
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cargas")

    def __str__(self):
        """Retorna una descripción breve de la carga."""
        return f"{self.descripcion} - {self.peso_kg} kg"


class Ruta(models.Model):
    """
    Modelo que define una ruta de transporte.
    """
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    tipo_transporte = models.CharField(max_length=15, choices=TIPO_TRANSPORTE)
    distancia_km = models.IntegerField(default=0)  # Distancia aproximada en kilómetros

    def __str__(self):
        """Retorna el origen y destino de la ruta."""
        return f"{self.origen} → {self.destino}"


class Despacho(models.Model):
    """
    Modelo principal que representa un despacho o envío.
    Vincula carga, ruta, vehículo/aeronave y conductor/piloto.
    """
    codigo = models.CharField(max_length=20, unique=True)  # Código único de seguimiento
    fecha = models.DateField()
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    
    # Relaciones opcionales dependiendo del tipo de transporte
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    aeronave = models.ForeignKey(Aeronave, on_delete=models.SET_NULL, null=True, blank=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True, blank=True)
    piloto = models.ForeignKey(Piloto, on_delete=models.SET_NULL, null=True, blank=True)
    
    estado = models.CharField(max_length=15, choices=ESTADO_DESPACHO, default='PENDIENTE')

    def __str__(self):
        """Retorna el código del despacho."""
        return self.codigo
