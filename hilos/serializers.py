from rest_framework import serializers
from .models import Hilo, Categoria, Respuesta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"
    
    def validate_nombre(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("El nombre de la categoría es obligatorio.")
        categoria_id = self.instance.id if self.instance else None
        if Categoria.objects.filter(nombre__iexact=value).exclude(id=categoria_id).exists():
            raise serializers.ValidationError("El nombre de la categoría ya existe.")        
        return value


class HiloSerializer(serializers.ModelSerializer):
    categoria_info = CategoriaSerializer(source="categoria", read_only=True)
    class Meta:
        model = Hilo
        fields = [
            "id",
            "titulo",
            "contenido",
            "fecha",
            "usuario",
            "categoria",
            "categoria_info",
        ]
        read_only_fields = ["fecha"]

    def validate_titulo(self, value):
        if not value:
            raise serializers.ValidationError("El título es obligatorio.")
        if len(value) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = [
            "id",
            "contenido",
            "usuario",
            "hilo",
            "fecha",
        ]
        read_only_fields = ["fecha"]

    def validate_contenido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El contenido de la respuesta es obligatorio.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El contenido debe tener al menos 3 caracteres.")
        return value.strip()