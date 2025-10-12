"""
URL configuration for maya_backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('usuarios.urls')),
    path('api/', include('contenido.urls')),
    path('api/', include('evaluaciones.urls')),
    path('api/', include('reportes.urls')),
]
