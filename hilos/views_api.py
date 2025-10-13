from rest_framework import viewsets, permissions, decorators, response, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Hilo, Categoria
from .serializers import HiloSerializer

class HiloViewSet(viewsets.ModelViewSet):
    queryset = Hilo.objects.select_related("usuario", "categoria").all()
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

    @decorators.action(detail=True, methods=["put"], url_path="cambiar-categoria")
    def cambiar_categoria(self, request, pk=None):
        hilo = self.get_object()
        categoria_id = request.data.get("categoria_id")
        if not categoria_id:
            return response.Response({"detail": "categoria_id es requerido"}, status=400)
        try:
            nueva_categoria = Categoria.objects.get(pk=categoria_id)
        except Categoria.DoesNotExist:
            return response.Response({"detail": "Categoría no existe"}, status=404)

        hilo.categoria = nueva_categoria
        hilo.save()
        return response.Response(self.get_serializer(hilo).data, status=status.HTTP_200_OK)
