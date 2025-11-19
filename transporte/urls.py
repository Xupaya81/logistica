from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    VehiculoViewSet, AeronaveViewSet, ConductorViewSet, PilotoViewSet,
    ClienteViewSet, CargaViewSet, RutaViewSet, DespachoViewSet
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
