from django.urls import path
from .views import (
    ReporteListView,
    ReporteDetailView
)

urlpatterns = [
    # Reportes
    path('reportes/', ReporteListView.as_view(), name='reporte-list'),
    path('reportes/<str:id>/', ReporteDetailView.as_view(), name='reporte-detail'),
]
