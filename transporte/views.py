"""Vistas y viewsets para la app `transporte`.

Contiene ViewSets para la API REST y vistas que renderizan
plantillas HTML para el frontend Bootstrap.
"""

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Aeronave, Carga, Cliente, Conductor, Despacho,
    Piloto, Ruta, Vehiculo,
)

from .serializers import (
    AeronaveSerializer, CargaSerializer, ClienteSerializer,
    ConductorSerializer, DespachoSerializer, PilotoSerializer,
    RutaSerializer, VehiculoSerializer,
)


# ============================================================
# VIEWSETS PRINCIPALES
# ============================================================

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_transporte', 'patente', 'marca']
    search_fields = ['patente', 'marca', 'modelo']
    ordering_fields = ['patente', 'marca']


class AeronaveViewSet(viewsets.ModelViewSet):
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['codigo', 'modelo']


class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]  # protegido según rúbrica
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'apellido', 'licencia']


class PilotoViewSet(viewsets.ModelViewSet):
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer
    permission_classes = [IsAuthenticated]  # protegido según rúbrica
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'apellido', 'certificacion']


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['rut']
    search_fields = ['nombre', 'rut']


class CargaViewSet(viewsets.ModelViewSet):
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tipo', 'cliente']
    search_fields = ['descripcion']


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['origen', 'destino', 'tipo_transporte']
    search_fields = ['origen', 'destino']


class DespachoViewSet(viewsets.ModelViewSet):
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer
    permission_classes = [IsAuthenticated]  # protegido según rúbrica

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['ruta', 'estado', 'vehiculo', 'aeronave']
    search_fields = ['codigo']



# ============================================================
# VISTAS ADICIONALES (HTML)

def home(request):
    """Renderiza el panel principal del frontend (Bootstrap)."""
    return render(request, "home.html")


def despachos_html(request):
    """Renderiza la lista de despachos usando `despachos.html`."""
    contexto = {"despachos": Despacho.objects.all()}
    return render(request, "despachos.html", contexto)


def rutas_html(request):
    """Renderiza la vista de rutas."""
    return render(request, "rutas.html", {"rutas": Ruta.objects.all()})


def clientes_html(request):
    """Renderiza la vista de clientes."""
    return render(request, "clientes.html", {"clientes": Cliente.objects.all()})
