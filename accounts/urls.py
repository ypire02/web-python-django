from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.perfil_editar, name='perfil_editar'),
    path('perfil/password/', views.cambiar_password, name='cambiar_password'),
]
