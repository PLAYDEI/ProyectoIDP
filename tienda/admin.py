from django.contrib import admin
from .models import Producto

# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "marca", "tipo_producto", "precio", "producto_popular")
    search_fields = ("nombre", "marca")
    list_filter = ("marca", "tipo_producto", "producto_popular")