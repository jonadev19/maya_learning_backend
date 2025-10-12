from rest_framework import serializers
from bson import ObjectId
from usuarios.serializers import ObjectIdField


class ReporteGeneradoSerializer(serializers.Serializer):
    """Serializer para ReporteGenerado"""
    id = ObjectIdField(source='_id', read_only=True)
    tipo = serializers.ChoiceField(
        choices=['individual', 'grupo', 'tema', 'general']
    )
    generado_por_id = ObjectIdField()
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    alumno_id = ObjectIdField(required=False, allow_null=True)
    grupo_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tema_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    archivo_url = serializers.URLField(required=False, allow_blank=True)
    metadatos = serializers.DictField(required=False)
    fecha_generacion = serializers.DateTimeField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)


class ReporteGeneradoCreateSerializer(serializers.Serializer):
    """Serializer para crear ReporteGenerado"""
    tipo = serializers.ChoiceField(
        choices=['individual', 'grupo', 'tema', 'general']
    )
    generado_por_id = ObjectIdField()
    titulo = serializers.CharField(max_length=200)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    alumno_id = ObjectIdField(required=False, allow_null=True)
    grupo_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tema_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    archivo_url = serializers.URLField(required=False, allow_blank=True)
    metadatos = serializers.DictField(required=False)


class GenerarReporteIndividualSerializer(serializers.Serializer):
    """Serializer para generar reporte individual de alumno"""
    alumno_id = ObjectIdField()
    tema_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fecha_inicio = serializers.DateField(required=False, allow_null=True)
    fecha_fin = serializers.DateField(required=False, allow_null=True)


class GenerarReporteGrupoSerializer(serializers.Serializer):
    """Serializer para generar reporte de grupo"""
    grupo_nombre = serializers.CharField()
    tema_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fecha_inicio = serializers.DateField(required=False, allow_null=True)
    fecha_fin = serializers.DateField(required=False, allow_null=True)


class GenerarReporteTemaSerializer(serializers.Serializer):
    """Serializer para generar reporte de tema"""
    tema_nombre = serializers.CharField()
    grupo_nombre = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fecha_inicio = serializers.DateField(required=False, allow_null=True)
    fecha_fin = serializers.DateField(required=False, allow_null=True)
