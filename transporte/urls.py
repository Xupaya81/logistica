"""Ruteo de la API REST para la app `transporte`.

Expone los ViewSets a través de un `DefaultRouter`.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AeronaveViewSet, CargaViewSet, ClienteViewSet, ConductorViewSet,
    DespachoViewSet, PilotoViewSet, RutaViewSet, VehiculoViewSet,
)

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'aeronaves', AeronaveViewSet)
router.register(r'conductores', ConductorViewSet)
router.register(r'pilotos', PilotoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'cargas', CargaViewSet)
router.register(r'rutas', RutaViewSet)
router.register(r'despachos', DespachoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
