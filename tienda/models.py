from django.db import models

# Opciones para categorizar productos
TIPOS_PRODUCTOS = [
    ('herramienta', 'Herramienta'),
    ('material', 'Material'),
    ('electrico', 'Eléctrico'),
    ('pintura', 'Pintura'),
]

MARCAS = [
    ('bosch', 'Bosch'),
    ('stanley', 'Stanley'),
    ('dewalt', 'DeWalt'),
    ('makita', 'Makita'),
]

# Modelo de productos
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_producto = models.CharField(max_length=20, choices=TIPOS_PRODUCTOS, default='herramienta')
    marca = models.CharField(max_length=20, choices=MARCAS, default='bosch')
    precio = models.IntegerField()
    producto_popular = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

    def formato_precio(self):
        return f"${self.precio:,}".replace(",", ".")
