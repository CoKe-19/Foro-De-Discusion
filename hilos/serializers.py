from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Categoria, Hilo

User = get_user_model()

class UsuarioMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class HiloSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioMiniSerializer(source='usuario', read_only=True)
    categoria_info = serializers.StringRelatedField(source='categoria', read_only=True)

    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())

    class Meta:
        model = Hilo
        fields = ['id', 'titulo', 'contenido', 'usuario', 'usuario_info', 'categoria', 'categoria_info', 'fecha']
