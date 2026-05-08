from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Autor, Libro, Prestamo
from .forms import AutorForm, LibroForm, PrestamoForm, BuscarLibroForm

# Solo usuarios staff (administradores/libreros) pueden hacer CRUD
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/accounts/login/')


# --- Home ---

def index(request):
    total_libros = Libro.objects.count()
    total_autores = Autor.objects.count()
    prestamos_activos = Prestamo.objects.filter(devuelto=False).count()
    libros_disponibles = Libro.objects.filter(cantidad_disponible__gt=0)
    prestamos_recientes = Prestamo.objects.filter(devuelto=False).select_related('libro')[:5]

    return render(request, 'catalogo/index.html', {
        'total_libros': total_libros,
        'total_autores': total_autores,
        'prestamos_activos': prestamos_activos,
        'libros_disponibles': libros_disponibles,
        'prestamos_recientes': prestamos_recientes,
    })


def about(request):
    return render(request, 'catalogo/about.html')


# --- Autores ---

def autores_lista(request):
    autores = Autor.objects.all()
    return render(request, 'catalogo/autores_lista.html', {'autores': autores})


@staff_required
def autor_agregar(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor agregado correctamente.')
            return redirect('autores_lista')
    else:
        form = AutorForm()
    return render(request, 'catalogo/autor_form.html', {'form': form, 'titulo': 'Agregar Autor'})


def autor_detalle(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    libros = autor.libros.all()
    return render(request, 'catalogo/autor_detalle.html', {'autor': autor, 'libros': libros})


@staff_required
def autor_editar(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autor actualizado correctamente.')
            return redirect('autor_detalle', pk=autor.pk)
    else:
        form = AutorForm(instance=autor)
    return render(request, 'catalogo/autor_form.html', {'form': form, 'titulo': 'Editar Autor'})


@staff_required
def autor_eliminar(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        messages.success(request, 'Autor eliminado correctamente.')
        return redirect('autores_lista')
    return render(request, 'catalogo/confirmar_eliminar.html', {
        'objeto': autor,
        'tipo': 'autor',
        'cancelar_url': 'autor_detalle',
        'pk': pk,
    })


# --- Libros (CBV) ---

class LibrosListaView(ListView):
    """Vista CBV para listar libros"""
    model = Libro
    template_name = 'catalogo/libros_lista.html'
    context_object_name = 'libros'

    def get_queryset(self):
        return Libro.objects.select_related('autor').all()


class LibroDetalleView(LoginRequiredMixin, DetailView):
    """Vista CBV con LoginRequiredMixin para ver detalle del libro"""
    model = Libro
    template_name = 'catalogo/libro_detalle.html'
    context_object_name = 'libro'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestamos'] = self.object.prestamos.filter(devuelto=False)
        return context


@staff_required
def libro_agregar(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro agregado correctamente.')
            return redirect('libros_lista')
    else:
        form = LibroForm()
    return render(request, 'catalogo/libro_form.html', {'form': form, 'titulo': 'Agregar Libro'})


@staff_required
def libro_editar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('libro_detalle', pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'catalogo/libro_form.html', {'form': form, 'titulo': 'Editar Libro'})


@staff_required
def libro_eliminar(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente.')
        return redirect('libros_lista')
    return render(request, 'catalogo/confirmar_eliminar.html', {
        'objeto': libro,
        'tipo': 'libro',
        'cancelar_url': 'libro_detalle',
        'pk': pk,
    })


def libros_buscar(request):
    form = BuscarLibroForm(request.GET)
    resultados = []
    consulta = ''
    if form.is_valid():
        consulta = form.cleaned_data.get('consulta', '')
        if consulta:
            resultados = (
                Libro.objects.filter(titulo__icontains=consulta) |
                Libro.objects.filter(autor__nombre__icontains=consulta)
            ).select_related('autor').distinct()
    return render(request, 'catalogo/buscar.html', {
        'form': form,
        'resultados': resultados,
        'consulta': consulta,
    })


# --- Préstamos ---

def prestamos_lista(request):
    prestamos = Prestamo.objects.select_related('libro').all()
    return render(request, 'catalogo/prestamos_lista.html', {'prestamos': prestamos})


@staff_required
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
                messages.success(request, 'Préstamo registrado correctamente.')
                return redirect('prestamos_lista')
            else:
                form.add_error('libro', 'Este libro no tiene ejemplares disponibles.')
    else:
        form = PrestamoForm()
    return render(request, 'catalogo/prestamo_form.html', {'form': form, 'titulo': 'Registrar Préstamo'})


@staff_required
def prestamo_devolver(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if not prestamo.devuelto:
        prestamo.devuelto = True
        prestamo.save()
        prestamo.libro.cantidad_disponible += 1
        prestamo.libro.save()
        messages.success(request, 'Devolución registrada correctamente.')
    return redirect('prestamos_lista')
