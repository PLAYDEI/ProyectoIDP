"""
URL configuration for Ferreteria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from tienda.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Vista de admin
    path('admin/', admin.site.urls),

    # Vistas generales
    path('', index, name='inicio'),
    path('carrito/', carrito, name='carrito'),
    path('productos/', productos, name='productos'),
    path('ubicacion/', ubicacion, name='ubicacion'),

    # API de productos
    path('api/productos/', lista_productos, name='api_productos'),

    # Transbank
    path("iniciar_pago/", iniciar_pago, name="iniciar_pago"),  # Ruta para procesar el pago con Webpay
    path("pago_exitoso/", lambda req: render(req, "pago_exitoso.html")),  # Vista simple para mostrar éxito del pago
 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)