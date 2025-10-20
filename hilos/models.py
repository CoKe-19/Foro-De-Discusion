from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    imagen = models.ImageField(upload_to='hilos_imagenes/', blank=True, null=True)

class Respuesta(models.Model):
    contenido = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="respuestas")
    hilo = models.ForeignKey(Hilo, on_delete=models.CASCADE, related_name="respuestas")
    fecha = models.DateField(auto_now_add=True)

    def likes_count(self):
        return self.likes.count()

    def ya_like(self, user):
        return self.likes.filter(usuario=user).exists()

    class Meta:
        ordering = ["fecha"]

    def __str__(self):
        return self.contenido

class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name='likes')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'respuesta')
        
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    apodo = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    hilos_creados = models.PositiveIntegerField(default=0)
    comentarios = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()

class Video(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='videos/', null=True, blank=True) 
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo