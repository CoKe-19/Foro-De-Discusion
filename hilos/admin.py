from django.contrib import admin
from .models import Hilo, Respuesta, Categoria

# Register your models here.
admin.site.register(Hilo)
admin.site.register(Respuesta)
admin.site.register(Categoria)