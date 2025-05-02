from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'tipo_producto', 'marca', 'precio', 'producto_popular', 'foto']