from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import Actividad, IntentoPrueba, Calificacion
from .serializers import (
    ActividadSerializer,
    ActividadCreateSerializer,
    PreguntaCreateSerializer,
    IntentoPruebaSerializer,
    IntentoPruebaCreateSerializer,
    RegistrarRespuestaSerializer,
    CalificacionSerializer,
    EstadisticasSerializer
)


class ActividadListView(APIView):
    """
    GET /api/actividades/ - Lista todas las actividades
    POST /api/actividades/ - Crea una nueva actividad
    """

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

    def post(self, request):
        serializer = ActividadCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            actividad_id = Actividad.crear(
                tema_id=serializer.validated_data['tema_id'],
                nivel=serializer.validated_data['nivel'],
                titulo=serializer.validated_data['titulo'],
                descripcion=serializer.validated_data['descripcion'],
                tipo=serializer.validated_data.get('tipo', 'opcion_multiple'),
                duracion_minutos=serializer.validated_data.get('duracion_minutos'),
                orden=serializer.validated_data.get('orden', 0)
            )
            actividad = Actividad.obtener_por_id(actividad_id)
            response_serializer = ActividadSerializer(actividad)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


class ActividadPreguntasView(APIView):
    """POST /api/actividades/<id>/preguntas/ - Agrega una pregunta a una actividad"""

    def post(self, request, id):
        serializer = PreguntaCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            Actividad.agregar_pregunta(
                actividad_id=id,
                pregunta_texto=serializer.validated_data['texto'],
                respuesta_correcta=serializer.validated_data['respuesta_correcta'],
                opciones=serializer.validated_data.get('opciones', []),
                puntos=serializer.validated_data.get('puntos', 1),
                tipo=serializer.validated_data.get('tipo', 'opcion_multiple')
            )
            actividad = Actividad.obtener_por_id(id)
            response_serializer = ActividadSerializer(actividad)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IntentoPruebaCreateView(APIView):
    """POST /api/intentos/ - Crea un nuevo intento de prueba"""

    def post(self, request):
        serializer = IntentoPruebaCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            intento_id = IntentoPrueba.crear(
                alumno_id=serializer.validated_data['alumno_id'],
                actividad_id=serializer.validated_data['actividad_id']
            )
            intento = IntentoPrueba.obtener_por_id(intento_id)
            response_serializer = IntentoPruebaSerializer(intento)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IntentoRespuestasView(APIView):
    """POST /api/intentos/<id>/respuestas/ - Registra una respuesta en un intento"""

    def post(self, request, id):
        serializer = RegistrarRespuestaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            intento = IntentoPrueba.obtener_por_id(id)
            if not intento:
                return Response(
                    {'error': 'Intento no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Obtener la actividad para verificar la respuesta
            actividad = Actividad.obtener_por_id(intento['actividad_id'])
            pregunta_id = serializer.validated_data['pregunta_id']
            respuesta_alumno = serializer.validated_data['respuesta_alumno']

            # Buscar la pregunta en la actividad
            pregunta = next(
                (p for p in actividad.get('preguntas', []) if p['id'] == pregunta_id),
                None
            )

            if not pregunta:
                return Response(
                    {'error': 'Pregunta no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verificar si la respuesta es correcta
            es_correcta = respuesta_alumno.strip().lower() == pregunta['respuesta_correcta'].strip().lower()
            puntos_obtenidos = pregunta['puntos'] if es_correcta else 0

            # Registrar la respuesta
            IntentoPrueba.registrar_respuesta(
                intento_id=id,
                pregunta_id=pregunta_id,
                respuesta_alumno=respuesta_alumno,
                es_correcta=es_correcta,
                puntos_obtenidos=puntos_obtenidos
            )

            intento = IntentoPrueba.obtener_por_id(id)
            response_serializer = IntentoPruebaSerializer(intento)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IntentoFinalizarView(APIView):
    """POST /api/intentos/<id>/finalizar/ - Finaliza un intento y genera calificación"""

    def post(self, request, id):
        try:
            intento = IntentoPrueba.obtener_por_id(id)
            if not intento:
                return Response(
                    {'error': 'Intento no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if intento['estado'] == 'completada':
                return Response(
                    {'error': 'El intento ya fue completado'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Finalizar intento
            IntentoPrueba.finalizar_intento(id)

            # Crear calificación automáticamente
            calificacion_id = Calificacion.crear_desde_intento(id)
            calificacion = Calificacion.obtener_por_id(calificacion_id)

            response_serializer = CalificacionSerializer(calificacion)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CalificacionCreateView(APIView):
    """POST /api/calificaciones/ - Crea una calificación desde un intento"""

    def post(self, request):
        intento_id = request.data.get('intento_id')

        if not intento_id:
            return Response(
                {'error': 'intento_id es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            calificacion_id = Calificacion.crear_desde_intento(intento_id)
            calificacion = Calificacion.obtener_por_id(calificacion_id)
            serializer = CalificacionSerializer(calificacion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
