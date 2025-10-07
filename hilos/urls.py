"""
URL configuration for forodediscusion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .import views

urlpatterns = [
    path('', views.pagina_principal ,name="pagina_principal"),
    path('crear_hilo/', views.registrar_hilo ,name="registrar_hilo"),
    path('lista/', views.lista_hilos, name="lista_hilos"),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('hilos/<int:hilo_id>/', views.detalle_hilo, name='detalle_hilo'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('hilos/<int:hilo_id>/eliminar/', views.eliminar_hilo, name='eliminar_hilo'),
    path('mis-hilos/', views.mis_hilos, name='mis_hilos'),
    path('hilo/<int:hilo_id>/editar/', views.editar_hilo, name='editar_hilo'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('administrar_hilos/', views.administrar_hilos, name='administrar_hilos'),
    path('respuestas/<int:respuesta_id>/eliminar/', views.eliminar_respuesta, name='eliminar_respuesta'),
    path('respuestas/<int:respuesta_id>/editar/', views.editar_respuesta, name='editar_respuesta'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),
    path('respuestas/<int:respuesta_id>/like/', views.like_respuesta, name='like_respuesta'),
    path('perfil/completar/', views.completar_perfil, name='completar_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),

]
