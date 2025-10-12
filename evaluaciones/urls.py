from django.urls import path
from .views import (
    ActividadListView,
    ActividadDetailView,
    IntentoPruebaListView,
    IntentoPruebaDetailView,
    CalificacionListView,
    CalificacionDetailView,
    PromedioAlumnoView,
    PromedioGrupoView,
    EstadisticasTemaView
)

urlpatterns = [
    # Actividades
    path('actividades/', ActividadListView.as_view(), name='actividad-list'),
    path('actividades/<str:id>/', ActividadDetailView.as_view(), name='actividad-detail'),

    # Intentos
    path('intentos/', IntentoPruebaListView.as_view(), name='intento-list'),
    path('intentos/<str:id>/', IntentoPruebaDetailView.as_view(), name='intento-detail'),

    # Calificaciones
    path('calificaciones/', CalificacionListView.as_view(), name='calificacion-list'),
    path('calificaciones/<str:id>/', CalificacionDetailView.as_view(), name='calificacion-detail'),
    path('calificaciones/promedio/<str:alumno_id>/', PromedioAlumnoView.as_view(), name='promedio-alumno'),
    path('calificaciones/promedio-grupo/<str:grupo_nombre>/', PromedioGrupoView.as_view(), name='promedio-grupo'),
    path('calificaciones/estadisticas/<str:tema_nombre>/', EstadisticasTemaView.as_view(), name='estadisticas-tema'),
]
