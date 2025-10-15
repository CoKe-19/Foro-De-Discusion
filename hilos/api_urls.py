from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views_api import HiloViewSet ,CategoriaViewSet , RespuestaViewSet

router = DefaultRouter()
router.register("hilos", HiloViewSet, basename="hilo")
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("respuestas", RespuestaViewSet, basename="respuesta")


urlpatterns = [
    path("", include(router.urls)),
]
