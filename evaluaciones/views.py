from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import Actividad, IntentoPrueba, Calificacion
from .serializers import (
    ActividadSerializer,
    IntentoPruebaSerializer,
    CalificacionSerializer,
    EstadisticasSerializer
)


class ActividadListView(APIView):
    """GET /api/actividades/ - Lista todas las actividades"""

    def get(self, request):
        # Filtros opcionales
        tema_id = request.query_params.get('tema_id', None)
        nivel = request.query_params.get('nivel', None)

        if tema_id and nivel:
            actividades = Actividad.listar_por_tema_y_nivel(tema_id, nivel)
        elif tema_id:
            actividades = Actividad.listar_por_tema(tema_id)
        else:
            actividades = Actividad.find({'activo': True})

        serializer = ActividadSerializer(actividades, many=True)
        return Response(serializer.data)


class ActividadDetailView(APIView):
    """GET /api/actividades/<id>/ - Detalle de una actividad"""

    def get(self, request, id):
        try:
            actividad = Actividad.obtener_por_id(id)
            if not actividad:
                return Response(
                    {'error': 'Actividad no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ActividadSerializer(actividad)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class IntentoPruebaListView(APIView):
    """GET /api/intentos/ - Lista intentos de prueba"""

    def get(self, request):
        # Filtros opcionales
        alumno_id = request.query_params.get('alumno_id', None)
        actividad_id = request.query_params.get('actividad_id', None)

        if alumno_id:
            intentos = IntentoPrueba.listar_por_alumno(alumno_id)
        elif actividad_id:
            intentos = IntentoPrueba.listar_por_actividad(actividad_id)
        else:
            intentos = IntentoPrueba.find({})

        serializer = IntentoPruebaSerializer(intentos, many=True)
        return Response(serializer.data)


class IntentoPruebaDetailView(APIView):
    """GET /api/intentos/<id>/ - Detalle de un intento"""

    def get(self, request, id):
        try:
            intento = IntentoPrueba.obtener_por_id(id)
            if not intento:
                return Response(
                    {'error': 'Intento no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = IntentoPruebaSerializer(intento)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CalificacionListView(APIView):
    """GET /api/calificaciones/ - Lista calificaciones"""

    def get(self, request):
        # Filtros opcionales
        alumno_id = request.query_params.get('alumno_id', None)
        grupo_nombre = request.query_params.get('grupo', None)
        tema_nombre = request.query_params.get('tema', None)
        actividad_id = request.query_params.get('actividad_id', None)

        if alumno_id:
            calificaciones = Calificacion.listar_por_alumno(alumno_id)
        elif grupo_nombre:
            calificaciones = Calificacion.listar_por_grupo(grupo_nombre)
        elif tema_nombre:
            calificaciones = Calificacion.listar_por_tema(tema_nombre)
        elif actividad_id:
            calificaciones = Calificacion.listar_por_actividad(actividad_id)
        else:
            calificaciones = Calificacion.find({})

        serializer = CalificacionSerializer(calificaciones, many=True)
        return Response(serializer.data)


class CalificacionDetailView(APIView):
    """GET /api/calificaciones/<id>/ - Detalle de una calificación"""

    def get(self, request, id):
        try:
            calificacion = Calificacion.obtener_por_id(id)
            if not calificacion:
                return Response(
                    {'error': 'Calificación no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = CalificacionSerializer(calificacion)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PromedioAlumnoView(APIView):
    """GET /api/calificaciones/promedio/<alumno_id>/ - Promedio de un alumno"""

    def get(self, request, alumno_id):
        try:
            tema_nombre = request.query_params.get('tema', None)
            promedio = Calificacion.obtener_promedio_alumno(alumno_id, tema_nombre)

            return Response({
                'alumno_id': alumno_id,
                'tema_nombre': tema_nombre,
                'promedio': promedio
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PromedioGrupoView(APIView):
    """GET /api/calificaciones/promedio-grupo/<grupo_nombre>/ - Promedio de un grupo"""

    def get(self, request, grupo_nombre):
        try:
            tema_nombre = request.query_params.get('tema', None)
            promedio = Calificacion.obtener_promedio_grupo(grupo_nombre, tema_nombre)

            return Response({
                'grupo_nombre': grupo_nombre,
                'tema_nombre': tema_nombre,
                'promedio': promedio
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class EstadisticasTemaView(APIView):
    """GET /api/calificaciones/estadisticas/<tema_nombre>/ - Estadísticas de un tema"""

    def get(self, request, tema_nombre):
        try:
            grupo_nombre = request.query_params.get('grupo', None)
            estadisticas = Calificacion.obtener_estadisticas_tema(tema_nombre, grupo_nombre)

            serializer = EstadisticasSerializer(estadisticas)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
