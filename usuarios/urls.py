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
from .authentication import (
    LoginView,
    CustomTokenRefreshView,
    LogoutView,
    MeView
)

urlpatterns = [
    # Autenticación
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),

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
