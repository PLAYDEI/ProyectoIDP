import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from django.views.decorators.csrf import csrf_exempt  # Decorador para evitar errores CSRF en desarrollo
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions  # SDK Transbank para transacciones
from transbank.common.integration_type import IntegrationType  # Tipo de entorno (TEST o LIVE)
from transbank.common.options import WebpayOptions  
from transbank.error.transbank_error import TransbankError  # Para capturar errores del SDK

# Vistas generales
def index(request):
    productos_qs = Producto.objects.filter(producto_popular=True)  # <–– campo correcto
    productos = list(
        productos_qs.values('id', 'nombre', 'precio', 'foto')
    )
    return render(request, 'index.html', {
        'producto_popular': json.dumps(productos)
    })

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
            "id": p.id,
            "nombre": p.nombre,
            "tipo_producto": p.tipo_producto,
            "marca": p.marca,
            "precio": p.precio,
            "foto": p.foto.url if p.foto else None
        }
        for p in productos
    ]
    return JsonResponse(productos_json, safe=False)

# CRUD - LISTAR
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
# Transbank
@csrf_exempt
def iniciar_pago(request):
    if request.method == "POST":
        datos = json.loads(request.body)  # Convierte el JSON del body en diccionario Python
        productos = datos.get("productos", [])  # Extrae los productos seleccionados

        if not productos:
            return JsonResponse({"error": "No se seleccionaron productos."}, status=400)

        # Calcula el total sumando los precios de los productos
        try:
            total = sum(round(float(p["precio"])) for p in productos)
        except (ValueError, KeyError, TypeError) as e:
            return JsonResponse({"error": f"Precio inválido: {str(e)}"}, status=400)

        # Define datos requeridos por Transbank para iniciar la transacción
        buy_order = f"orden{request.META['REMOTE_ADDR'].replace('.', '')}"  # Crea orden basada en IP
        session_id = "session123"  # Valor fijo, pero se puede personalizar
        return_url = "http://127.0.0.1:8000/pago_exitoso/"  # URL a la que redirige Transbank tras pagar

        # Configura opciones del entorno de integración de Transbank
        options = WebpayOptions(
            commerce_code="597055555532",  # Código de comercio de prueba
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",  # API Key de prueba
            integration_type=IntegrationType.TEST  # Ambiente de prueba
        )

        transaction = Transaction(options)  # Crea instancia para transacción

        try:
            # Llama al SDK de Transbank para crear la transacción
            response = transaction.create(buy_order, session_id, total, return_url)
            return JsonResponse({
                "url_webpay": response['url'] + "?token_ws=" + response['token'],
                "token": response['token']
            })
        except TransbankError as e:
            print("❌ Error en la creación del pago:", e.message)
            return JsonResponse({"error": e.message}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)