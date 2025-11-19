from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Vistas HTML
from transporte import views as tviews

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Logística Global API",
        default_version='v1',
        description="Documentación de la API Logística",
    ),
    public=True,
)



urlpatterns = [

    # ===========================
    # API REST Framework
    # ===========================
    path('', include('transporte.urls')),

    # ===========================
    # ADMIN
    # ===========================
    path('admin/', admin.site.urls),

    # ===========================
    # JWT
    # ===========================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ===========================
    # SWAGGER
    # ===========================
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('openapi/', schema_view.without_ui(cache_timeout=0), name='openapi-schema'),

    # ===========================
    # FRONT-END (HTML)
    # ===========================

    # HOME
    path('site/', tviews.home, name='home'),

    # ---------- CLIENTES ----------
    path('site/clientes/', tviews.clientes_html, name='clientes_list'),
    path('site/clientes/crear/', tviews.clientes_crear, name='clientes_crear'),
    path('site/clientes/editar/<int:id>/', tviews.clientes_editar, name='clientes_editar'),
    path('site/clientes/eliminar/<int:id>/', tviews.clientes_eliminar, name='clientes_eliminar'),

    # ---------- RUTAS ----------
    path('site/rutas/', tviews.rutas_html, name='rutas_list'),
    path('site/rutas/crear/', tviews.rutas_crear, name='rutas_crear'),
    path('site/rutas/editar/<int:id>/', tviews.rutas_editar, name='rutas_editar'),
    path('site/rutas/eliminar/<int:id>/', tviews.rutas_eliminar, name='rutas_eliminar'),

    # ---------- DESPACHOS ----------
    path('site/despachos/', tviews.despachos_html, name='despachos_list'),
    path('site/despachos/crear/', tviews.despachos_crear, name='despachos_crear'),
    path('site/despachos/editar/<int:id>/', tviews.despachos_editar, name='despachos_editar'),
    path('site/despachos/eliminar/<int:id>/', tviews.despachos_eliminar, name='despachos_eliminar'),

    # ---------- VEHÍCULOS ----------
    path('site/vehiculos/', tviews.vehiculos_list, name='vehiculos_list'),
    path('site/vehiculos/crear/', tviews.vehiculos_crear, name='vehiculos_crear'),
    path('site/vehiculos/editar/<int:id>/', tviews.vehiculos_editar, name='vehiculos_editar'),
    path('site/vehiculos/eliminar/<int:id>/', tviews.vehiculos_eliminar, name='vehiculos_eliminar'),

    # ---------- AERONAVES ----------
    path('site/aeronaves/', tviews.aeronaves_list, name='aeronaves_list'),
    path('site/aeronaves/crear/', tviews.aeronaves_crear, name='aeronaves_crear'),
    path('site/aeronaves/editar/<int:id>/', tviews.aeronaves_editar, name='aeronaves_editar'),
    path('site/aeronaves/eliminar/<int:id>/', tviews.aeronaves_eliminar, name='aeronaves_eliminar'),

    # ---------- CARGAS ----------
    path('site/cargas/', tviews.cargas_list, name='cargas_list'),
    path('site/cargas/crear/', tviews.cargas_crear, name='cargas_crear'),
    path('site/cargas/editar/<int:id>/', tviews.cargas_editar, name='cargas_editar'),
    path('site/cargas/eliminar/<int:id>/', tviews.cargas_eliminar, name='cargas_eliminar'),

    # ---------- CONDUCTORES ----------
    path('site/conductores/', tviews.conductores_list, name='conductores_list'),
    path('site/conductores/crear/', tviews.conductores_crear, name='conductores_crear'),
    path('site/conductores/editar/<int:id>/', tviews.conductores_editar, name='conductores_editar'),
    path('site/conductores/eliminar/<int:id>/', tviews.conductores_eliminar, name='conductores_eliminar'),

    # ---------- PILOTOS ----------
    path('site/pilotos/', tviews.pilotos_list, name='pilotos_list'),
    path('site/pilotos/crear/', tviews.pilotos_crear, name='pilotos_crear'),
    path('site/pilotos/editar/<int:id>/', tviews.pilotos_editar, name='pilotos_editar'),
    path('site/pilotos/eliminar/<int:id>/', tviews.pilotos_eliminar, name='pilotos_eliminar'),
]
