from rest_framework import serializers
from .models import Vehiculo, Aeronave, Conductor, Piloto, Cliente, Carga, Ruta, Despacho


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class AeronaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aeronave
        fields = '__all__'


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'


class PilotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piloto
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class CargaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Carga
        fields = '__all__'


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'


class DespachoSerializer(serializers.ModelSerializer):
    ruta_info = RutaSerializer(source='ruta', read_only=True)
    carga_info = CargaSerializer(source='carga', read_only=True)

    vehiculo_info = VehiculoSerializer(source='vehiculo', read_only=True)
    aeronave_info = AeronaveSerializer(source='aeronave', read_only=True)
    conductor_info = ConductorSerializer(source='conductor', read_only=True)
    piloto_info = PilotoSerializer(source='piloto', read_only=True)

    class Meta:
        model = Despacho
        fields = '__all__'
