from django import forms
from .models import Autor, Libro, Prestamo


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'pais', 'anio_nacimiento']
        labels = {
            'nombre': 'Nombre completo',
            'pais': 'País de origen',
            'anio_nacimiento': 'Año de nacimiento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Gabriel García Márquez'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Colombia'}),
            'anio_nacimiento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1927'}),
        }


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'isbn', 'numero_catalogo', 'anio_publicacion', 'cantidad_disponible', 'imagen', 'autor']
        labels = {
            'titulo': 'Título del libro',
            'isbn': 'ISBN',
            'numero_catalogo': 'Número de catálogo',
            'anio_publicacion': 'Año de publicación',
            'cantidad_disponible': 'Cantidad disponible',
            'imagen': 'Portada del libro',
            'autor': 'Autor',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cien años de soledad'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 9780307474728'}),
            'numero_catalogo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1001'}),
            'anio_publicacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1967'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-select'}),
        }


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['libro', 'usuario_nombre', 'fecha_devolucion']
        labels = {
            'libro': 'Libro a prestar',
            'usuario_nombre': 'Nombre del usuario',
            'fecha_devolucion': 'Fecha de devolución',
        }
        widgets = {
            'libro': forms.Select(attrs={'class': 'form-select'}),
            'usuario_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
            'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BuscarLibroForm(forms.Form):
    consulta = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título o autor...',
        })
    )
