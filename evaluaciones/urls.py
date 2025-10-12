from django.urls import path
from .views import (
    ActividadListView,
    ActividadDetailView,
    ActividadPreguntasView,
    IntentoPruebaListView,
    IntentoPruebaDetailView,
    IntentoPruebaCreateView,
    IntentoRespuestasView,
    IntentoFinalizarView,
    CalificacionListView,
    CalificacionDetailView,
    CalificacionCreateView,
    PromedioAlumnoView,
    PromedioGrupoView,
    EstadisticasTemaView
)

urlpatterns = [
    # Actividades
    path('actividades/', ActividadListView.as_view(), name='actividad-list'),
    path('actividades/<str:id>/', ActividadDetailView.as_view(), name='actividad-detail'),
    path('actividades/<str:id>/preguntas/', ActividadPreguntasView.as_view(), name='actividad-preguntas'),

    # Intentos
    path('intentos/', IntentoPruebaListView.as_view(), name='intento-list'),
    path('intentos/crear/', IntentoPruebaCreateView.as_view(), name='intento-create'),
    path('intentos/<str:id>/', IntentoPruebaDetailView.as_view(), name='intento-detail'),
    path('intentos/<str:id>/respuestas/', IntentoRespuestasView.as_view(), name='intento-respuestas'),
    path('intentos/<str:id>/finalizar/', IntentoFinalizarView.as_view(), name='intento-finalizar'),

    # Calificaciones
    path('calificaciones/', CalificacionListView.as_view(), name='calificacion-list'),
    path('calificaciones/crear/', CalificacionCreateView.as_view(), name='calificacion-create'),
    path('calificaciones/<str:id>/', CalificacionDetailView.as_view(), name='calificacion-detail'),
    path('calificaciones/promedio/<str:alumno_id>/', PromedioAlumnoView.as_view(), name='promedio-alumno'),
    path('calificaciones/promedio-grupo/<str:grupo_nombre>/', PromedioGrupoView.as_view(), name='promedio-grupo'),
    path('calificaciones/estadisticas/<str:tema_nombre>/', EstadisticasTemaView.as_view(), name='estadisticas-tema'),
]
