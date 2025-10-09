from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Categoria, Hilo, Respuesta
from .serializers import CategoriaSerializer, HiloSerializer, RespuestaSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class HiloViewSet(viewsets.ModelViewSet):
    queryset = Hilo.objects.all()
    serializer_class = HiloSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RespuestaViewSet(viewsets.ModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@api_view(['GET'])
def saludo(request):
    return Response({"mensaje": "¡Hola desde tu primera API RESTful!"})
