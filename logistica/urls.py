"""
URL configuration for logistica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from transporte.views import home, despachos_html, rutas_html, clientes_html


# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Logística Global API",
        default_version='v1',
        description="Documentación de la API Logística",
    ),
    public=True,
)

urlpatterns = [

    # API (montada en root) y vistas HTML bajo 'site/' para evitar colisiones
    path('', include('transporte.urls')),

    # Páginas HTML (interfaz Bootstrap) - accesibles bajo /site/
    path('site/', home),
    path('site/despachos', despachos_html),
    path('site/rutas', rutas_html),
    path('site/clientes', clientes_html),

    # Admin
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('openapi/', schema_view.without_ui(cache_timeout=0), name='openapi-schema'),
]
