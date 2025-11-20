from rest_framework import serializers
from .models import Vehiculo, Aeronave, Conductor, Piloto, Cliente, Carga, Ruta, Despacho


class VehiculoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Vehiculo.
    Convierte objetos Vehiculo a JSON y viceversa.
    """
    class Meta:
        model = Vehiculo
        fields = '__all__'


class AeronaveSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Aeronave.
    """
    class Meta:
        model = Aeronave
        fields = '__all__'


class ConductorSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Conductor.
    """
    class Meta:
        model = Conductor
        fields = '__all__'


class PilotoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Piloto.
    """
    class Meta:
        model = Piloto
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Cliente.
    """
    class Meta:
        model = Cliente
        fields = '__all__'


class CargaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Carga.
    Incluye el nombre del cliente como campo de solo lectura.
    """
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Carga
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Ruta.
    """
    class Meta:
        model = Ruta
        fields = '__all__'


class DespachoSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Despacho.
    Incluye información anidada de las relaciones (ruta, carga, vehículo, etc.)
    para facilitar la visualización en el frontend.
    """
    # Campos anidados de solo lectura para mostrar detalles completos en la respuesta API
    ruta_info = RutaSerializer(source='ruta', read_only=True)
    carga_info = CargaSerializer(source='carga', read_only=True)

    vehiculo_info = VehiculoSerializer(source='vehiculo', read_only=True)
    aeronave_info = AeronaveSerializer(source='aeronave', read_only=True)
    conductor_info = ConductorSerializer(source='conductor', read_only=True)
    piloto_info = PilotoSerializer(source='piloto', read_only=True)

    class Meta:
        model = Despacho
        fields = '__all__'
