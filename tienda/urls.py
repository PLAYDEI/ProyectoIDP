from django.urls import path
from . import views

urlpatterns = [
    
    path('gestionar/', views.gestionar_productos, name='gestionar_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]