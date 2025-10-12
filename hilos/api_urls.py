from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views_api import HiloViewSet

router = DefaultRouter()
router.register("hilos", HiloViewSet, basename="hilo")

urlpatterns = [
    path("", include(router.urls)),
]
