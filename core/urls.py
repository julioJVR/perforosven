from django.urls import path
from . import views, views_usuarios

app_name = 'core'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # URLs de gestión de usuarios
    path('usuarios/', views_usuarios.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views_usuarios.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:user_id>/editar/', views_usuarios.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/password/', views_usuarios.cambiar_password, name='cambiar_password'),
    path('usuarios/<int:user_id>/toggle/', views_usuarios.toggle_usuario, name='toggle_usuario'),
    path('usuarios/<int:user_id>/detalle/', views_usuarios.detalle_usuario, name='detalle_usuario'),
]