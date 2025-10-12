from rest_framework import serializers
from bson import ObjectId
from usuarios.serializers import ObjectIdField


class TemaSerializer(serializers.Serializer):
    """Serializer para Tema"""
    id = ObjectIdField(source='_id', read_only=True)
    nombre = serializers.ChoiceField(
        choices=['Números', 'Comidas', 'Objetos Cotidianos', 'Animales']
    )
    descripcion = serializers.CharField(required=False, allow_blank=True)
    orden = serializers.IntegerField(default=0)
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class TemaCreateSerializer(serializers.Serializer):
    """Serializer para crear Tema"""
    nombre = serializers.ChoiceField(
        choices=['Números', 'Comidas', 'Objetos Cotidianos', 'Animales']
    )
    descripcion = serializers.CharField(required=False, allow_blank=True)
    orden = serializers.IntegerField(default=0)


class RecursoSerializer(serializers.Serializer):
    """Serializer para recursos multimedia"""
    url = serializers.URLField()
    tipo = serializers.ChoiceField(choices=['imagen', 'audio', 'video'])
    descripcion = serializers.CharField(required=False, allow_blank=True)
    agregado_en = serializers.DateTimeField(read_only=True)


class MaterialSerializer(serializers.Serializer):
    """Serializer para Material"""
    id = ObjectIdField(source='_id', read_only=True)
    tema_id = ObjectIdField()
    tema_nombre = serializers.CharField(read_only=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )
    titulo = serializers.CharField(max_length=200)
    contenido = serializers.CharField()
    recursos = RecursoSerializer(many=True, required=False)
    orden = serializers.IntegerField(default=0)
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class MaterialCreateSerializer(serializers.Serializer):
    """Serializer para crear Material"""
    tema_id = ObjectIdField()
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )
    titulo = serializers.CharField(max_length=200)
    contenido = serializers.CharField()
    recursos = RecursoSerializer(many=True, required=False)
    orden = serializers.IntegerField(default=0)


class MaterialUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar Material"""
    tema_id = ObjectIdField(required=False)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        required=False
    )
    titulo = serializers.CharField(max_length=200, required=False)
    contenido = serializers.CharField(required=False)
    orden = serializers.IntegerField(required=False)
    activo = serializers.BooleanField(required=False)


class VocabularioSerializer(serializers.Serializer):
    """Serializer para Vocabulario"""
    id = ObjectIdField(source='_id', read_only=True)
    tema_id = ObjectIdField()
    tema_nombre = serializers.CharField(read_only=True)
    palabra_maya = serializers.CharField(max_length=100)
    palabra_espanol = serializers.CharField(max_length=100)
    pronunciacion = serializers.CharField(max_length=100, required=False, allow_blank=True)
    imagen_url = serializers.URLField(required=False, allow_blank=True)
    audio_url = serializers.URLField(required=False, allow_blank=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class VocabularioCreateSerializer(serializers.Serializer):
    """Serializer para crear Vocabulario"""
    tema_id = ObjectIdField()
    palabra_maya = serializers.CharField(max_length=100)
    palabra_espanol = serializers.CharField(max_length=100)
    pronunciacion = serializers.CharField(max_length=100, required=False, allow_blank=True)
    imagen_url = serializers.URLField(required=False, allow_blank=True)
    audio_url = serializers.URLField(required=False, allow_blank=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        default='Básico'
    )


class VocabularioUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar Vocabulario"""
    tema_id = ObjectIdField(required=False)
    palabra_maya = serializers.CharField(max_length=100, required=False)
    palabra_espanol = serializers.CharField(max_length=100, required=False)
    pronunciacion = serializers.CharField(max_length=100, required=False, allow_blank=True)
    imagen_url = serializers.URLField(required=False, allow_blank=True)
    audio_url = serializers.URLField(required=False, allow_blank=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        required=False
    )
    activo = serializers.BooleanField(required=False)
