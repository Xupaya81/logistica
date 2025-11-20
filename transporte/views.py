"""
Vistas y ViewSets para la app transporte.
Incluye:
- API REST (ViewSets)
- Vistas HTML (list, crear, editar, eliminar)
- Integración CRUD vía API usando requests
"""

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Vehiculo, Aeronave, Conductor, Piloto, Cliente,
    Carga, Ruta, Despacho
)

from .serializers import (
    VehiculoSerializer, AeronaveSerializer, ConductorSerializer, PilotoSerializer,
    ClienteSerializer, CargaSerializer, RutaSerializer, DespachoSerializer
)

# ==========================================
# CONFIG API LOCAL
# ==========================================

API_BASE = "http://127.0.0.1:8000/"


# ==========================================
# VIEWSETS DEL API (no tocar)
# ==========================================

class VehiculoViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Vehículos.
    Permite filtrar por tipo de transporte, patente y marca.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_transporte', 'patente', 'marca']
    search_fields = ['patente', 'marca', 'modelo']
    ordering_fields = ['patente', 'marca']


class AeronaveViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Aeronaves.
    """
    queryset = Aeronave.objects.all()
    serializer_class = AeronaveSerializer


class ConductorViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Conductores.
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer


class PilotoViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Pilotos.
    """
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Clientes.
    Permite búsqueda por nombre y RUT.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['rut']
    search_fields = ['nombre', 'rut']


class CargaViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Cargas.
    """
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer


class RutaViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Rutas.
    """
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer


class DespachoViewSet(viewsets.ModelViewSet):
    """
    API ViewSet para manejar operaciones CRUD de Despachos.
    """
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer


# ==========================================
# VISTAS HTML PRINCIPALES
# ==========================================

@login_required
def home(request):
    """
    Vista principal del dashboard.
    Recopila estadísticas de despachos, rutas, clientes y flota para mostrar en gráficos.
    Requiere autenticación.
    """
    try:
        # Consumir API para obtener conteos
        despachos = requests.get(API_BASE + "despachos/").json()
        rutas = requests.get(API_BASE + "rutas/").json()
        clientes = requests.get(API_BASE + "clientes/").json()
        vehiculos = requests.get(API_BASE + "vehiculos/").json()
        aeronaves = requests.get(API_BASE + "aeronaves/").json()

        # Datos para gráficos
        transport_types = [len(vehiculos), len(aeronaves)]
        
        # Agrupar despachos por estado (ejemplo simple)
        estados = {}
        for d in despachos:
            estado = d.get('estado', 'Desconocido')
            estados[estado] = estados.get(estado, 0) + 1
        
        despachos_labels = list(estados.keys())
        despachos_data = list(estados.values())

        context = {
            "despachos_count": len(despachos),
            "rutas_count": len(rutas),
            "clientes_count": sum(1 for c in clientes if c.get('activo')),
            "transport_types": transport_types,
            "despachos_labels": despachos_labels,
            "despachos_data": despachos_data,
        }
    except Exception:
        context = {
            "despachos_count": "-",
            "rutas_count": "-",
            "clientes_count": "-",
            "transport_types": [0, 0],
            "despachos_labels": [],
            "despachos_data": [],
        }
    
    return render(request, "home.html", context)


@login_required
def despachos_html(request):
    """Renderiza la lista de despachos."""
    return render(request, "despachos.html")


@login_required
def rutas_html(request):
    """Renderiza la lista de rutas."""
    return render(request, "rutas.html")


@login_required
def clientes_html(request):
    """Renderiza la lista de clientes."""
    return render(request, "clientes.html")


@login_required
def vehiculos_list(request):
    """Renderiza la lista de vehículos."""
    return render(request, "vehiculos.html")


@login_required
def aeronaves_list(request):
    """Renderiza la lista de aeronaves."""
    return render(request, "aeronaves.html")


@login_required
def conductores_list(request):
    """Renderiza la lista de conductores."""
    return render(request, "conductores.html")


@login_required
def pilotos_list(request):
    """Renderiza la lista de pilotos."""
    return render(request, "pilotos.html")


@login_required
def cargas_list(request):
    """Renderiza la lista de cargas."""
    return render(request, "cargas.html")


# ==========================================
# CRUD CLIENTES (HTML + API)
# ==========================================

@login_required
def clientes_crear(request):
    """
    Vista para crear un nuevo cliente.
    Maneja GET para mostrar el formulario y POST para enviar datos a la API.
    """
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "rut": request.POST.get("rut"),
            "correo": request.POST.get("correo"),
            "activo": request.POST.get("estado") == "1",
        }

        resp = requests.post(API_BASE + "clientes/", json=data)

        if resp.status_code == 201:
            messages.success(request, "Cliente creado exitosamente.")
            return redirect("clientes_list")

        messages.error(request, "Error al crear cliente.")
    
    return render(request, "clientes/crear.html")


@login_required
def clientes_editar(request, pk):
    """
    Vista para editar un cliente existente.
    Recupera datos actuales vía API y envía actualizaciones vía PUT.
    """
    # Obtener cliente desde la API
    cliente = requests.get(API_BASE + f"clientes/{pk}/").json()

    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "rut": request.POST.get("rut"),
            "correo": request.POST.get("correo"),
            "activo": True if request.POST.get("estado") == "1" else False,
        }

        resp = requests.put(API_BASE + f"clientes/{pk}/", json=data)

        if resp.status_code in (200, 202):
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("clientes_list")

        messages.error(request, "Error al actualizar cliente.")

    return render(request, "clientes/editar.html", {"cliente": cliente})


@login_required
def clientes_eliminar(request, pk):
    """
    Vista para eliminar un cliente.
    Solicita confirmación y ejecuta DELETE contra la API.
    """
    if request.method == "POST":

        resp = requests.delete(API_BASE + f"clientes/{pk}/")

        if resp.status_code in (200, 204):
            messages.success(request, "Cliente eliminado.")
            return redirect("clientes_list")

        messages.error(request, "Error al eliminar cliente.")

    cliente = requests.get(API_BASE + f"clientes/{pk}/").json()

    return render(request, "clientes/eliminar.html", {"cliente": cliente})


# ==========================================
# CRUD GENERALES (PLANTILLAS ESTÁTICAS)
# ==========================================

# ==========================================
# CRUD VEHICULOS
# ==========================================

@login_required
def vehiculos_crear(request):
    """
    Vista para crear un nuevo vehículo.
    """
    if request.method == "POST":
        data = {
            "patente": request.POST.get("patente"),
            "marca": request.POST.get("marca"),
            "modelo": request.POST.get("modelo"),
            "capacidad_kg": request.POST.get("capacidad_kg"),
            "tipo_transporte": request.POST.get("tipo_transporte"),
        }
        resp = requests.post(API_BASE + "vehiculos/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Vehículo creado exitosamente.")
            return redirect("vehiculos_list")
        messages.error(request, "Error al crear vehículo.")
    
    return render(request, "vehiculos/crear.html")


@login_required
def vehiculos_editar(request, pk):
    if request.method == "POST":
        data = {
            "patente": request.POST.get("patente"),
            "marca": request.POST.get("marca"),
            "modelo": request.POST.get("modelo"),
            "capacidad_kg": request.POST.get("capacidad_kg"),
            "tipo_transporte": request.POST.get("tipo_transporte"),
        }
        resp = requests.put(API_BASE + f"vehiculos/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Vehículo actualizado.")
            return redirect("vehiculos_list")
        messages.error(request, "Error al actualizar vehículo.")

    vehiculo = requests.get(API_BASE + f"vehiculos/{pk}/").json()
    return render(request, "vehiculos/editar.html", {"vehiculo": vehiculo})


@login_required
def vehiculos_eliminar(request, pk):
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"vehiculos/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Vehículo eliminado.")
            return redirect("vehiculos_list")
        messages.error(request, "Error al eliminar vehículo.")

    vehiculo = requests.get(API_BASE + f"vehiculos/{pk}/").json()
    return render(request, "vehiculos/eliminar.html", {"vehiculo": vehiculo})


# ==========================================
# CRUD AERONAVES
# ==========================================

@login_required
def aeronaves_crear(request):
    """
    Vista para crear una nueva aeronave.
    """
    if request.method == "POST":
        data = {
            "codigo": request.POST.get("codigo"),
            "modelo": request.POST.get("modelo"),
            "capacidad_kg": request.POST.get("capacidad_kg"),
        }
        resp = requests.post(API_BASE + "aeronaves/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Aeronave creada exitosamente.")
            return redirect("aeronaves_list")
        messages.error(request, "Error al crear aeronave.")
    return render(request, "aeronaves/crear.html")

@login_required
def aeronaves_editar(request, pk):
    """
    Vista para editar una aeronave existente.
    """
    if request.method == "POST":
        data = {
            "codigo": request.POST.get("codigo"),
            "modelo": request.POST.get("modelo"),
            "capacidad_kg": request.POST.get("capacidad_kg"),
        }
        resp = requests.put(API_BASE + f"aeronaves/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Aeronave actualizada.")
            return redirect("aeronaves_list")
        messages.error(request, "Error al actualizar aeronave.")

    aeronave = requests.get(API_BASE + f"aeronaves/{pk}/").json()
    return render(request, "aeronaves/editar.html", {"aeronave": aeronave})

@login_required
def aeronaves_eliminar(request, pk):
    """
    Vista para eliminar una aeronave.
    """
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"aeronaves/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Aeronave eliminada.")
            return redirect("aeronaves_list")
        messages.error(request, "Error al eliminar aeronave.")

    aeronave = requests.get(API_BASE + f"aeronaves/{pk}/").json()
    return render(request, "aeronaves/eliminar.html", {"aeronave": aeronave})


# ==========================================
# CRUD CONDUCTORES
# ==========================================

@login_required
def conductores_crear(request):
    """
    Vista para crear un nuevo conductor.
    """
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "licencia": request.POST.get("licencia"),
            "vigente": request.POST.get("vigente") == "1",
        }
        resp = requests.post(API_BASE + "conductores/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Conductor creado exitosamente.")
            return redirect("conductores_list")
        messages.error(request, "Error al crear conductor.")
    return render(request, "conductores/crear.html")

@login_required
def conductores_editar(request, pk):
    """
    Vista para editar un conductor existente.
    """
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "licencia": request.POST.get("licencia"),
            "vigente": request.POST.get("vigente") == "1",
        }
        resp = requests.put(API_BASE + f"conductores/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Conductor actualizado.")
            return redirect("conductores_list")
        messages.error(request, "Error al actualizar conductor.")

    conductor = requests.get(API_BASE + f"conductores/{pk}/").json()
    return render(request, "conductores/editar.html", {"conductor": conductor})

@login_required
def conductores_eliminar(request, pk):
    """
    Vista para eliminar un conductor.
    """
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"conductores/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Conductor eliminado.")
            return redirect("conductores_list")
        messages.error(request, "Error al eliminar conductor.")

    conductor = requests.get(API_BASE + f"conductores/{pk}/").json()
    return render(request, "conductores/eliminar.html", {"conductor": conductor})


# ==========================================
# CRUD PILOTOS
# ==========================================

@login_required
def pilotos_crear(request):
    """
    Vista para crear un nuevo piloto.
    """
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "certificacion": request.POST.get("certificacion"),
            "vigente": request.POST.get("vigente") == "1",
        }
        resp = requests.post(API_BASE + "pilotos/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Piloto creado exitosamente.")
            return redirect("pilotos_list")
        messages.error(request, "Error al crear piloto.")
    return render(request, "pilotos/crear.html")

@login_required
def pilotos_editar(request, pk):
    """
    Vista para editar un piloto existente.
    """
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "apellido": request.POST.get("apellido"),
            "certificacion": request.POST.get("certificacion"),
            "vigente": request.POST.get("vigente") == "1",
        }
        resp = requests.put(API_BASE + f"pilotos/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Piloto actualizado.")
            return redirect("pilotos_list")
        messages.error(request, "Error al actualizar piloto.")

    piloto = requests.get(API_BASE + f"pilotos/{pk}/").json()
    return render(request, "pilotos/editar.html", {"piloto": piloto})

@login_required
def pilotos_eliminar(request, pk):
    """
    Vista para eliminar un piloto.
    """
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"pilotos/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Piloto eliminado.")
            return redirect("pilotos_list")
        messages.error(request, "Error al eliminar piloto.")

    piloto = requests.get(API_BASE + f"pilotos/{pk}/").json()
    return render(request, "pilotos/eliminar.html", {"piloto": piloto})


# ==========================================
# CRUD CARGAS
# ==========================================

@login_required
def cargas_crear(request):
    """
    Vista para crear una nueva carga.
    Requiere seleccionar un cliente existente.
    """
    if request.method == "POST":
        data = {
            "descripcion": request.POST.get("descripcion"),
            "peso_kg": request.POST.get("peso_kg"),
            "tipo": request.POST.get("tipo"),
            "valor": request.POST.get("valor"),
            "cliente": request.POST.get("cliente"),
        }
        resp = requests.post(API_BASE + "cargas/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Carga creada exitosamente.")
            return redirect("cargas_list")
        messages.error(request, "Error al crear carga.")
    
    clientes = requests.get(API_BASE + "clientes/").json()
    return render(request, "cargas/crear.html", {"clientes": clientes})

@login_required
def cargas_editar(request, pk):
    """
    Vista para editar una carga existente.
    """
    if request.method == "POST":
        data = {
            "descripcion": request.POST.get("descripcion"),
            "peso_kg": request.POST.get("peso_kg"),
            "tipo": request.POST.get("tipo"),
            "valor": request.POST.get("valor"),
            "cliente": request.POST.get("cliente"),
        }
        resp = requests.put(API_BASE + f"cargas/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Carga actualizada.")
            return redirect("cargas_list")
        messages.error(request, "Error al actualizar carga.")

    carga = requests.get(API_BASE + f"cargas/{pk}/").json()
    clientes = requests.get(API_BASE + "clientes/").json()
    return render(request, "cargas/editar.html", {"carga": carga, "clientes": clientes})

@login_required
def cargas_eliminar(request, pk):
    """
    Vista para eliminar una carga.
    """
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"cargas/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Carga eliminada.")
            return redirect("cargas_list")
        messages.error(request, "Error al eliminar carga.")

    carga = requests.get(API_BASE + f"cargas/{pk}/").json()
    return render(request, "cargas/eliminar.html", {"carga": carga})


# ==========================================
# CRUD RUTAS
# ==========================================

@login_required
def rutas_crear(request):
    """
    Vista para crear una nueva ruta.
    """
    if request.method == "POST":
        data = {
            "origen": request.POST.get("origen"),
            "destino": request.POST.get("destino"),
            "tipo_transporte": request.POST.get("tipo_transporte"),
            "distancia_km": request.POST.get("distancia_km"),
        }
        resp = requests.post(API_BASE + "rutas/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Ruta creada exitosamente.")
            return redirect("rutas_list")
        messages.error(request, "Error al crear ruta.")
    return render(request, "rutas/crear.html")

@login_required
def rutas_editar(request, pk):
    """
    Vista para editar una ruta existente.
    """
    if request.method == "POST":
        data = {
            "origen": request.POST.get("origen"),
            "destino": request.POST.get("destino"),
            "tipo_transporte": request.POST.get("tipo_transporte"),
            "distancia_km": request.POST.get("distancia_km"),
        }
        resp = requests.put(API_BASE + f"rutas/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Ruta actualizada.")
            return redirect("rutas_list")
        messages.error(request, "Error al actualizar ruta.")

    ruta = requests.get(API_BASE + f"rutas/{pk}/").json()
    return render(request, "rutas/editar.html", {"ruta": ruta})

@login_required
def rutas_eliminar(request, pk):
    """
    Vista para eliminar una ruta.
    """
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"rutas/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Ruta eliminada.")
            return redirect("rutas_list")
        messages.error(request, "Error al eliminar ruta.")

    ruta = requests.get(API_BASE + f"rutas/{pk}/").json()
    return render(request, "rutas/eliminar.html", {"ruta": ruta})


# ==========================================
# CRUD DESPACHOS
# ==========================================

@login_required
def despachos_crear(request):
    """
    Vista para crear un nuevo despacho.
    Requiere cargar listas de rutas, cargas, vehículos, etc. para los selectores.
    """
    if request.method == "POST":
        data = {
            "codigo": request.POST.get("codigo"),
            "fecha": request.POST.get("fecha"),
            "ruta": request.POST.get("ruta"),
            "carga": request.POST.get("carga"),
            "vehiculo": request.POST.get("vehiculo") or None,
            "aeronave": request.POST.get("aeronave") or None,
            "conductor": request.POST.get("conductor") or None,
            "piloto": request.POST.get("piloto") or None,
            "estado": request.POST.get("estado"),
        }
        resp = requests.post(API_BASE + "despachos/", json=data)
        if resp.status_code == 201:
            messages.success(request, "Despacho creado exitosamente.")
            return redirect("despachos_list")
        messages.error(request, "Error al crear despacho.")

    context = {
        "rutas": requests.get(API_BASE + "rutas/").json(),
        "cargas": requests.get(API_BASE + "cargas/").json(),
        "vehiculos": requests.get(API_BASE + "vehiculos/").json(),
        "aeronaves": requests.get(API_BASE + "aeronaves/").json(),
        "conductores": requests.get(API_BASE + "conductores/").json(),
        "pilotos": requests.get(API_BASE + "pilotos/").json(),
    }
    return render(request, "despachos/crear.html", context)

@login_required
def despachos_editar(request, pk):
    """
    Vista para editar un despacho existente.
    """
    if request.method == "POST":
        data = {
            "codigo": request.POST.get("codigo"),
            "fecha": request.POST.get("fecha"),
            "ruta": request.POST.get("ruta"),
            "carga": request.POST.get("carga"),
            "vehiculo": request.POST.get("vehiculo") or None,
            "aeronave": request.POST.get("aeronave") or None,
            "conductor": request.POST.get("conductor") or None,
            "piloto": request.POST.get("piloto") or None,
            "estado": request.POST.get("estado"),
        }
        resp = requests.put(API_BASE + f"despachos/{pk}/", json=data)
        if resp.status_code in (200, 202):
            messages.success(request, "Despacho actualizado.")
            return redirect("despachos_list")
        messages.error(request, "Error al actualizar despacho.")

    despacho = requests.get(API_BASE + f"despachos/{pk}/").json()
    context = {
        "despacho": despacho,
        "rutas": requests.get(API_BASE + "rutas/").json(),
        "cargas": requests.get(API_BASE + "cargas/").json(),
        "vehiculos": requests.get(API_BASE + "vehiculos/").json(),
        "aeronaves": requests.get(API_BASE + "aeronaves/").json(),
        "conductores": requests.get(API_BASE + "conductores/").json(),
        "pilotos": requests.get(API_BASE + "pilotos/").json(),
    }
    return render(request, "despachos/editar.html", context)


@login_required
def despachos_eliminar(request, pk):
    """
    Vista para eliminar un despacho.
    """
    # Eliminar despacho
    if request.method == "POST":
        resp = requests.delete(API_BASE + f"despachos/{pk}/")
        if resp.status_code in (200, 204):
            messages.success(request, "Despacho eliminado.")
            return redirect("despachos_list")
        messages.error(request, "Error al eliminar despacho.")

    despacho = requests.get(API_BASE + f"despachos/{pk}/").json()
    return render(request, "despachos/eliminar.html", {"despacho": despacho})
