from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Hilo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="hilos")
    titulo = models.CharField(max_length=150)
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="hilos")

class Respuesta(models.Model):
    contenido = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="respuestas")
    hilo = models.ForeignKey(Hilo, on_delete=models.CASCADE, related_name="respuestas")
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["fecha"]

    def __str__(self):
        return self.contenido

