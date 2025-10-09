from rest_framework import serializers
from .models import Categoria, Hilo, Respuesta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class HiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hilo
        fields = '__all__'

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'
