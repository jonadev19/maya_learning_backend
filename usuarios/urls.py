from django.urls import path
from .views import (
    GrupoListView,
    GrupoDetailView,
    AdministradorListView,
    AdministradorDetailView,
    AlumnoListView,
    AlumnoDetailView,
    UsuarioListView,
    UsuarioDetailView
)

urlpatterns = [
    # Grupos
    path('grupos/', GrupoListView.as_view(), name='grupo-list'),
    path('grupos/<str:id>/', GrupoDetailView.as_view(), name='grupo-detail'),

    # Administradores
    path('administradores/', AdministradorListView.as_view(), name='admin-list'),
    path('administradores/<str:id>/', AdministradorDetailView.as_view(), name='admin-detail'),

    # Alumnos
    path('alumnos/', AlumnoListView.as_view(), name='alumno-list'),
    path('alumnos/<str:id>/', AlumnoDetailView.as_view(), name='alumno-detail'),

    # Usuarios generales
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('usuarios/<str:id>/', UsuarioDetailView.as_view(), name='usuario-detail'),
]
