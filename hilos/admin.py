from django.contrib import admin
from .models import Hilo, Respuesta, Categoria , Video
# Register your models here.
admin.site.register(Hilo)
admin.site.register(Respuesta)
admin.site.register(Categoria)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'autor__username')