from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #CRUD
    path('gestionar/', views.gestionar_productos, name='gestionar_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]