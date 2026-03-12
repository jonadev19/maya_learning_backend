"""
URL configuration for maya_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/health/', health_check),

    # API endpoints
    path('api/', include('usuarios.urls')),
    path('api/', include('contenido.urls')),
    path('api/', include('evaluaciones.urls')),
    path('api/', include('reportes.urls')),
]
