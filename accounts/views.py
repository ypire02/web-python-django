from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .forms import SignupForm, EditarUsuarioForm, EditarPerfilForm, CambiarPasswordForm
from .models import Perfil


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Perfil.objects.create(usuario=user)
                login(request, user)
                messages.success(request, f'¡Bienvenida, {user.username}! Tu cuenta fue creada exitosamente.')
                return redirect('index')
            except IntegrityError:
                form.add_error('username', 'Ya existe un usuario con ese nombre. Elegí otro.')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Hola de nuevo, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Cerraste sesión correctamente.')
    return redirect('index')


@login_required
def perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'accounts/perfil.html', {'perfil': perfil})


@login_required
def perfil_editar(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        usuario_form = EditarUsuarioForm(request.POST, instance=request.user)
        perfil_form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        usuario_form = EditarUsuarioForm(instance=request.user)
        perfil_form = EditarPerfilForm(instance=perfil)
    return render(request, 'accounts/perfil_editar.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
    })


@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('perfil')
    else:
        form = CambiarPasswordForm(request.user)
    return render(request, 'accounts/cambiar_password.html', {'form': form})
