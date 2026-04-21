from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Autor, Libro, Prestamo
from .forms import AutorForm, LibroForm, PrestamoForm, BuscarLibroForm


def index(request):
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    prestamos_activos = Prestamo.objects.filter(devuelto=False).count()
    libros_disponibles = Libro.objects.filter(cantidad_disponible__gt=0)
    prestamos_recientes = Prestamo.objects.filter(devuelto=False).select_related('libro')[:5]

    contexto = {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'prestamos_activos': prestamos_activos,
        'libros_disponibles': libros_disponibles,
        'prestamos_recientes': prestamos_recientes,
    }
    return render(request, 'catalogo/index.html', contexto)


# --- Autores ---

def autores_lista(request):
    autores = Autor.objects.all()
    return render(request, 'catalogo/autores_lista.html', {'autores': autores})


def autor_agregar(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('autores_lista')
    else:
        form = AutorForm()
    return render(request, 'catalogo/autor_form.html', {'form': form, 'titulo': 'Agregar Autor'})


def autor_detalle(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    libros = autor.libros.all()
    return render(request, 'catalogo/autor_detalle.html', {'autor': autor, 'libros': libros})


# --- Libros ---

def libros_lista(request):
    libros = Libro.objects.select_related('autor').all()
    return render(request, 'catalogo/libros_lista.html', {'libros': libros})


def libro_agregar(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libros_lista')
    else:
        form = LibroForm()
    return render(request, 'catalogo/libro_form.html', {'form': form, 'titulo': 'Agregar Libro'})


def libro_detalle(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    prestamos = libro.prestamos.filter(devuelto=False)
    return render(request, 'catalogo/libro_detalle.html', {'libro': libro, 'prestamos': prestamos})


def libros_buscar(request):
    form = BuscarLibroForm(request.GET)
    resultados = []
    consulta = ''

    if form.is_valid():
        consulta = form.cleaned_data.get('consulta', '')
        if consulta:
            resultados = Libro.objects.filter(
                titulo__icontains=consulta
            ) | Libro.objects.filter(
                autor__nombre__icontains=consulta
            )
            resultados = resultados.select_related('autor').distinct()

    return render(request, 'catalogo/buscar.html', {
        'form': form,
        'resultados': resultados,
        'consulta': consulta,
    })


# --- Préstamos ---

def prestamos_lista(request):
    prestamos = Prestamo.objects.select_related('libro').all()
    return render(request, 'catalogo/prestamos_lista.html', {'prestamos': prestamos})


def prestamo_registrar(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            libro = prestamo.libro
            if libro.cantidad_disponible > 0:
                libro.cantidad_disponible -= 1
                libro.save()
                prestamo.save()
                return redirect('prestamos_lista')
            else:
                form.add_error('libro', 'Este libro no tiene ejemplares disponibles.')
    else:
        form = PrestamoForm()
    return render(request, 'catalogo/prestamo_form.html', {'form': form, 'titulo': 'Registrar Préstamo'})


def prestamo_devolver(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if not prestamo.devuelto:
        prestamo.devuelto = True
        prestamo.save()
        libro = prestamo.libro
        libro.cantidad_disponible += 1
        libro.save()
    return redirect('prestamos_lista')
