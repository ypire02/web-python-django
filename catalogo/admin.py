from django.contrib import admin
from .models import Autor, Libro, Prestamo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'anio_nacimiento']
    search_fields = ['nombre', 'pais']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'anio_publicacion', 'cantidad_disponible']
    list_filter = ['autor']
    search_fields = ['titulo', 'isbn']


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['usuario_nombre', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'devuelto']
    list_filter = ['devuelto']
    search_fields = ['usuario_nombre']
