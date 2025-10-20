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
from . import views


urlpatterns = [

    # ===========================
    # 🏠 PÁGINA PRINCIPAL
    # ===========================
    path('', views.pagina_principal, name='pagina_principal'),

    # ===========================
    # 👤 USUARIOS
    # ===========================
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('perfil/completar/', views.completar_perfil, name='completar_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),

    # ===========================
    # 💬 HILOS (FORO)
    # ===========================
    path('hilos/', views.lista_hilos, name='lista_hilos'),
    path('hilos/mis/', views.mis_hilos, name='mis_hilos'),
    path('hilos/crear/', views.registrar_hilo, name='hilo_crear'),
    path('hilos/<int:hilo_id>/', views.detalle_hilo, name='detalle_hilo'),
    path('hilos/<int:hilo_id>/editar/', views.editar_hilo, name='editar_hilo'),
    path('hilos/<int:hilo_id>/eliminar/', views.eliminar_hilo, name='eliminar_hilo'),
    path('administrar_hilos/', views.administrar_hilos, name='administrar_hilos'),

    # ===========================
    # 💭 RESPUESTAS (COMENTARIOS)
    # ===========================
    path('respuestas/<int:respuesta_id>/editar/', views.editar_respuesta, name='respuesta_editar'),
    path('respuestas/<int:respuesta_id>/eliminar/', views.eliminar_respuesta, name='respuesta_eliminar'),
    path('like/<int:respuesta_id>/', views.toggle_like, name='toggle_like'),

    # ===========================
    # 🗂️ CATEGORÍAS
    # ===========================
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='categoria_crear'),
    path('categorias/<int:categoria_id>/editar/', views.editar_categoria, name='categoria_editar'),
    path('categorias/<int:categoria_id>/eliminar/', views.eliminar_categoria, name='categoria_eliminar'),
    path('categoria/<int:categoria_id>/', views.filtrar_categoria, name='filtrar_categoria'),

    # ===========================
    # 🔎 BÚSQUEDA GLOBAL
    # ===========================
    path('buscar/', views.buscar, name='buscar'),

    # ===========================
    # 📚 PÁGINAS INFORMATIVAS
    # ===========================
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('guias/', views.guias, name='guias'),
    path('faq/', views.faq, name='faq'),
    path('reglas/', views.reglas, name='reglas'),
    path('acuerdo/', views.acuerdo, name='acuerdo'),
    path('politica/', views.politica, name='politica'),
]