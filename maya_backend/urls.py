"""
URL configuration for maya_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
import datetime


def health_check(request):
    mongo_status = "ok"
    try:
        if settings.MONGO_CLIENT is None:
            raise Exception("No hay cliente MongoDB")
        settings.MONGO_CLIENT.server_info()
    except Exception as e:
        mongo_status = f"error: {str(e)}"

    status = "ok" if mongo_status == "ok" else "degraded"
    http_status = 200 if status == "ok" else 503

    return JsonResponse(
        {
            "status": status,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "services": {
                "api": "ok",
                "mongodb": mongo_status,
            },
        },
        status=http_status,
    )


urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check
    path('api/health/', health_check),

    # API endpoints
    path('api/', include('usuarios.urls')),
    path('api/', include('contenido.urls')),
    path('api/', include('evaluaciones.urls')),
    path('api/', include('reportes.urls')),
]
