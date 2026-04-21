from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Autores
    path('autores/', views.autores_lista, name='autores_lista'),
    path('autores/agregar/', views.autor_agregar, name='autor_agregar'),
    path('autores/<int:pk>/', views.autor_detalle, name='autor_detalle'),

    # Libros
    path('libros/', views.libros_lista, name='libros_lista'),
    path('libros/agregar/', views.libro_agregar, name='libro_agregar'),
    path('libros/<int:pk>/', views.libro_detalle, name='libro_detalle'),
    path('libros/buscar/', views.libros_buscar, name='libros_buscar'),

    # Préstamos
    path('prestamos/', views.prestamos_lista, name='prestamos_lista'),
    path('prestamos/registrar/', views.prestamo_registrar, name='prestamo_registrar'),
    path('prestamos/<int:pk>/devolver/', views.prestamo_devolver, name='prestamo_devolver'),
]
