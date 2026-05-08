from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # Autores
    path('autores/', views.autores_lista, name='autores_lista'),
    path('autores/agregar/', views.autor_agregar, name='autor_agregar'),
    path('autores/<int:pk>/', views.autor_detalle, name='autor_detalle'),
    path('autores/<int:pk>/editar/', views.autor_editar, name='autor_editar'),
    path('autores/<int:pk>/eliminar/', views.autor_eliminar, name='autor_eliminar'),

    # Libros (CBV)
    path('libros/', views.LibrosListaView.as_view(), name='libros_lista'),
    path('libros/agregar/', views.libro_agregar, name='libro_agregar'),
    path('libros/buscar/', views.libros_buscar, name='libros_buscar'),
    path('libros/<int:pk>/', views.LibroDetalleView.as_view(), name='libro_detalle'),
    path('libros/<int:pk>/editar/', views.libro_editar, name='libro_editar'),
    path('libros/<int:pk>/eliminar/', views.libro_eliminar, name='libro_eliminar'),

    # Préstamos
    path('prestamos/', views.prestamos_lista, name='prestamos_lista'),
    path('prestamos/registrar/', views.prestamo_registrar, name='prestamo_registrar'),
    path('prestamos/<int:pk>/devolver/', views.prestamo_devolver, name='prestamo_devolver'),
]
