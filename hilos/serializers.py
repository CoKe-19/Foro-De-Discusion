from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hilo, Categoria

User = get_user_model()

class UsuarioMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_staff"]

class CategoriaMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]

class HiloSerializer(serializers.ModelSerializer):
    usuario_info = UsuarioMiniSerializer(source="usuario", read_only=True)
    categoria_info = CategoriaMiniSerializer(source="categoria", read_only=True)

    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())

    class Meta:
        model = Hilo
        fields = [
            "id",
            "titulo",
            "contenido",
            "fecha",
            "usuario", "usuario_info",
            "categoria", "categoria_info",
        ]
        read_only_fields = ["fecha"]

    def validate_titulo(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value

    def validate(self, data):
        usuario = data.get("usuario")
        categoria = data.get("categoria")
        if usuario and not usuario.is_active:
            raise serializers.ValidationError("El usuario está inactivo y no puede crear hilos.")
        if not categoria:
            raise serializers.ValidationError("Debe asignarse una categoría válida.")
        return data
