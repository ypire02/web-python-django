from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    anio_nacimiento = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nombre']


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    anio_publicacion = models.IntegerField()
    cantidad_disponible = models.IntegerField(default=1)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']


class Prestamo(models.Model):
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario_nombre = models.CharField(max_length=100)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario_nombre} - {self.libro.titulo}"

    class Meta:
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha_prestamo']
