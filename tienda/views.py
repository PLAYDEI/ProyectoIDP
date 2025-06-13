import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Models and forms
from .models import Producto
from .forms import ProductoForm

# Transbank SDK
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

# Vistas generales
def index(request):
    productos_qs = Producto.objects.filter(producto_popular=True)
    productos = list(productos_qs.values('id', 'nombre', 'precio', 'foto'))
    return render(request, 'index.html', {'producto_popular': json.dumps(productos)})


def carrito(request):
    return render(request, 'carrito.html')


def productos(request):
    return render(request, 'productos.html')


def ubicacion(request):
    return render(request, 'ubicacion.html')

# API de productos
def lista_productos(request):
    productos = Producto.objects.all()
    productos_json = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'tipo_producto': p.tipo_producto,
            'marca': p.marca,
            'precio': p.precio,
            'foto': p.foto.url if p.foto else None
        }
        for p in productos
    ]
    return JsonResponse(productos_json, safe=False)

# CRUD - LISTAR
@login_required
def gestionar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/gestionar.html', {'productos': productos})

# CRUD - AGREGAR
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestionar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/formulario.html', {'form': form, 'accion': 'Agregar'})

# CRUD - EDITAR
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestionar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/formulario.html', {'form': form, 'accion': 'Editar'})

# CRUD - ELIMINAR
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('gestionar_productos')

# --------------------- TRANSBANK PAYMENTS ---------------------
@csrf_exempt
def iniciar_pago(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    # Parsear JSON y validar
    try:
        datos = json.loads(request.body)
        productos = datos.get('productos', [])
    except (ValueError, TypeError):
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    if not productos:
        return JsonResponse({'error': 'No se seleccionaron productos.'}, status=400)

    # Calcular total
    try:
        total = sum(round(float(p['precio'])) for p in productos)
    except (KeyError, ValueError, TypeError) as e:
        return JsonResponse({'error': f'Precio inválido: {e}'}, status=400)

    # Datos de transacción
    buy_order = f"orden{request.META.get('REMOTE_ADDR', '').replace('.', '')}"
    session_id = 'session123'
    return_url = request.build_absolute_uri('/pago_exitoso/')

    # Configuración Webpay
    options = WebpayOptions(
        commerce_code='597055555532',
        api_key='579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        integration_type=IntegrationType.TEST
    )
    transaction = Transaction(options)

    try:
        resp = transaction.create(buy_order, session_id, total, return_url)
        return JsonResponse({
            'url_webpay': f"{resp['url']}?token_ws={resp['token']}",
            'token': resp['token']
        })
    except TransbankError as e:
        return JsonResponse({'error': e.message}, status=500)


def pago_exitoso(request):
    token_ws = request.GET.get('token_ws')
    return render(request, 'pago_exitoso.html', {'token': token_ws})

# --------------------- USUARIO ---------------------
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})
