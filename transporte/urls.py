"""Ruteo de la API REST para la app `transporte`.

Expone los ViewSets a través de un `DefaultRouter`.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
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

# Vistas HTML (sitio) — rutas nombradas para usar en templates
extra_patterns = [
    # Vehículos
    path('site/vehiculos/crear/', views.vehiculos_crear, name='vehiculos_crear'),
    path('site/vehiculos/<int:pk>/editar/', views.vehiculos_editar, name='vehiculos_editar'),
    path('site/vehiculos/<int:pk>/eliminar/', views.vehiculos_eliminar, name='vehiculos_eliminar'),

    # Aeronaves
    path('site/aeronaves/crear/', views.aeronaves_crear, name='aeronaves_crear'),
    path('site/aeronaves/<int:pk>/editar/', views.aeronaves_editar, name='aeronaves_editar'),
    path('site/aeronaves/<int:pk>/eliminar/', views.aeronaves_eliminar, name='aeronaves_eliminar'),

    # Conductores
    path('site/conductores/crear/', views.conductores_crear, name='conductores_crear'),
    path('site/conductores/<int:pk>/editar/', views.conductores_editar, name='conductores_editar'),
    path('site/conductores/<int:pk>/eliminar/', views.conductores_eliminar, name='conductores_eliminar'),

    # Pilotos
    path('site/pilotos/crear/', views.pilotos_crear, name='pilotos_crear'),
    path('site/pilotos/<int:pk>/editar/', views.pilotos_editar, name='pilotos_editar'),
    path('site/pilotos/<int:pk>/eliminar/', views.pilotos_eliminar, name='pilotos_eliminar'),

    # Clientes
    path('site/clientes/crear/', views.clientes_crear, name='clientes_crear'),
    path('site/clientes/<int:pk>/editar/', views.clientes_editar, name='clientes_editar'),
    path('site/clientes/<int:pk>/eliminar/', views.clientes_eliminar, name='clientes_eliminar'),

    # Cargas
    path('site/cargas/crear/', views.cargas_crear, name='cargas_crear'),
    path('site/cargas/<int:pk>/editar/', views.cargas_editar, name='cargas_editar'),
    path('site/cargas/<int:pk>/eliminar/', views.cargas_eliminar, name='cargas_eliminar'),

    # Rutas
    path('site/rutas/crear/', views.rutas_crear, name='rutas_crear'),
    path('site/rutas/<int:pk>/editar/', views.rutas_editar, name='rutas_editar'),
    path('site/rutas/<int:pk>/eliminar/', views.rutas_eliminar, name='rutas_eliminar'),

    # Despachos
    path('site/despachos/crear/', views.despachos_crear, name='despachos_crear'),
    path('site/despachos/<int:pk>/editar/', views.despachos_editar, name='despachos_editar'),
    path('site/despachos/<int:pk>/eliminar/', views.despachos_eliminar, name='despachos_eliminar'),
]

urlpatterns = [
    path('', include(router.urls)),
] + extra_patterns
