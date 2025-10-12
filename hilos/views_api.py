from rest_framework import viewsets, permissions, decorators, response, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hilo
from .serializers import HiloSerializer

class HiloViewSet(viewsets.ModelViewSet):
    queryset = Hilo.objects.all()
    serializer_class = HiloSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = {
        "categoria": ["exact"],
        "usuario": ["exact"],
        "fecha": ["gte", "lte"],
    }

    search_fields = [
        "titulo",
        "contenido",
        "usuario__username",
        "categoria__nombre",
    ]

    ordering_fields = ["fecha", "id"]
    ordering = ["-id"]

    @decorators.action(detail=True, methods=["put"], url_path="editar-titulo")
    def editar_titulo(self, request, pk=None):
        """
        PUT /api/hilos/{id}/editar-titulo/  body: {"titulo": "Nuevo título"}
        Actualiza solo el título del hilo.
        """
        hilo = self.get_object()
        nuevo_titulo = request.data.get("titulo")
        if not nuevo_titulo:
            return response.Response({"detail": "titulo es requerido"}, status=400)

        hilo.titulo = nuevo_titulo
        hilo.save()
        return response.Response(self.get_serializer(hilo).data)
