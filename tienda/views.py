from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto

# Vistas generales
def index(request):
    return render(request, 'index.html')

def carrito(request):
    return render(request, 'carrito.html')

# API de productos
def lista_productos(request):
    productos = Producto.objects.all()
    productos_json = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "tipo_producto": p.tipo_producto,
            "marca": p.marca,
            "precio": p.formato_precio(),
            "foto": p.foto.url if p.foto else None
        }
        for p in productos
    ]
    return JsonResponse(productos_json, safe=False)