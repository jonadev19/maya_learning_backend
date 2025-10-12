from rest_framework import serializers
from bson import ObjectId
from usuarios.serializers import ObjectIdField


class PreguntaSerializer(serializers.Serializer):
    """Serializer para Pregunta dentro de una Actividad"""
    id = serializers.CharField(read_only=True)
    texto = serializers.CharField()
    tipo = serializers.ChoiceField(
        choices=['opcion_multiple', 'emparejar', 'completar', 'escribir']
    )
    opciones = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    respuesta_correcta = serializers.CharField()
    puntos = serializers.IntegerField(default=1)
    orden = serializers.IntegerField(read_only=True)


class PreguntaCreateSerializer(serializers.Serializer):
    """Serializer para crear Pregunta"""
    texto = serializers.CharField()
    tipo = serializers.ChoiceField(
        choices=['opcion_multiple', 'emparejar', 'completar', 'escribir'],
        default='opcion_multiple'
    )
    opciones = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    respuesta_correcta = serializers.CharField()
    puntos = serializers.IntegerField(default=1)


class ActividadSerializer(serializers.Serializer):
    """Serializer para Actividad"""
    id = ObjectIdField(source='_id', read_only=True)
    tema_id = ObjectIdField()
    tema_nombre = serializers.CharField(read_only=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    tipo = serializers.ChoiceField(
        choices=['opcion_multiple', 'emparejar', 'completar', 'escribir']
    )
    duracion_minutos = serializers.IntegerField(required=False, allow_null=True)
    orden = serializers.IntegerField(default=0)
    preguntas = PreguntaSerializer(many=True, read_only=True)
    puntaje_total = serializers.IntegerField(read_only=True)
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class ActividadCreateSerializer(serializers.Serializer):
    """Serializer para crear Actividad"""
    tema_id = ObjectIdField()
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    tipo = serializers.ChoiceField(
        choices=['opcion_multiple', 'emparejar', 'completar', 'escribir'],
        default='opcion_multiple'
    )
    duracion_minutos = serializers.IntegerField(required=False, allow_null=True)
    orden = serializers.IntegerField(default=0)


class ActividadUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar Actividad"""
    tema_id = ObjectIdField(required=False)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        required=False
    )
    titulo = serializers.CharField(max_length=200, required=False)
    descripcion = serializers.CharField(required=False)
    tipo = serializers.ChoiceField(
        choices=['opcion_multiple', 'emparejar', 'completar', 'escribir'],
        required=False
    )
    duracion_minutos = serializers.IntegerField(required=False, allow_null=True)
    orden = serializers.IntegerField(required=False)
    activo = serializers.BooleanField(required=False)


class RespuestaSerializer(serializers.Serializer):
    """Serializer para Respuesta del alumno"""
    pregunta_id = serializers.CharField()
    respuesta_alumno = serializers.CharField()
    es_correcta = serializers.BooleanField(read_only=True)
    puntos_obtenidos = serializers.IntegerField(read_only=True)
    fecha_respuesta = serializers.DateTimeField(read_only=True)


class IntentoPruebaSerializer(serializers.Serializer):
    """Serializer para IntentoPrueba"""
    id = ObjectIdField(source='_id', read_only=True)
    alumno_id = ObjectIdField()
    alumno_nombre = serializers.CharField(read_only=True)
    alumno_email = serializers.CharField(read_only=True)
    grupo_nombre = serializers.CharField(read_only=True)
    actividad_id = ObjectIdField()
    actividad_titulo = serializers.CharField(read_only=True)
    tema_nombre = serializers.CharField(read_only=True)
    nivel = serializers.CharField(read_only=True)
    fecha_inicio = serializers.DateTimeField(read_only=True)
    fecha_finalizacion = serializers.DateTimeField(read_only=True, allow_null=True)
    estado = serializers.ChoiceField(
        choices=['en_progreso', 'completada', 'abandonada'],
        read_only=True
    )
    respuestas = RespuestaSerializer(many=True, read_only=True)
    puntaje_obtenido = serializers.IntegerField(read_only=True)
    puntaje_total = serializers.IntegerField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)


class IntentoPruebaCreateSerializer(serializers.Serializer):
    """Serializer para crear IntentoPrueba"""
    alumno_id = ObjectIdField()
    actividad_id = ObjectIdField()


class RegistrarRespuestaSerializer(serializers.Serializer):
    """Serializer para registrar una respuesta"""
    pregunta_id = serializers.CharField()
    respuesta_alumno = serializers.CharField()


class CalificacionSerializer(serializers.Serializer):
    """Serializer para Calificacion"""
    id = ObjectIdField(source='_id', read_only=True)
    alumno_id = ObjectIdField()
    alumno_nombre = serializers.CharField(read_only=True)
    alumno_email = serializers.CharField(read_only=True)
    grupo_nombre = serializers.CharField(read_only=True)
    actividad_id = ObjectIdField()
    actividad_titulo = serializers.CharField(read_only=True)
    tema_nombre = serializers.CharField(read_only=True)
    nivel = serializers.CharField(read_only=True)
    intento_id = ObjectIdField(read_only=True)
    puntaje_obtenido = serializers.IntegerField(read_only=True)
    puntaje_total = serializers.IntegerField(read_only=True)
    porcentaje = serializers.FloatField(read_only=True)
    aprobado = serializers.BooleanField(read_only=True)
    fecha_evaluacion = serializers.DateTimeField(read_only=True)
    duracion_minutos = serializers.FloatField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)


class EstadisticasSerializer(serializers.Serializer):
    """Serializer para Estadísticas de evaluaciones"""
    total_evaluaciones = serializers.IntegerField()
    promedio = serializers.FloatField()
    aprobados = serializers.IntegerField()
    reprobados = serializers.IntegerField()
    porcentaje_aprobacion = serializers.FloatField()


class PromedioAlumnoSerializer(serializers.Serializer):
    """Serializer para promedio de alumno"""
    alumno_id = ObjectIdField()
    tema_nombre = serializers.CharField(required=False, allow_null=True)
    promedio = serializers.FloatField()
