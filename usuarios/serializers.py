from rest_framework import serializers
from bson import ObjectId


class ObjectIdField(serializers.Field):
    """Campo personalizado para manejar ObjectId de MongoDB"""

    def to_representation(self, value):
        """Convierte ObjectId a string"""
        if isinstance(value, ObjectId):
            return str(value)
        return value

    def to_internal_value(self, data):
        """Convierte string a ObjectId"""
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError("ID inválido")


class GrupoSerializer(serializers.Serializer):
    """Serializer para Grupo"""
    id = ObjectIdField(source='_id', read_only=True)
    nombre = serializers.CharField(max_length=1)
    descripcion = serializers.CharField(required=False, allow_blank=True)
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class UsuarioSerializer(serializers.Serializer):
    """Serializer base para Usuario"""
    id = ObjectIdField(source='_id', read_only=True)
    email = serializers.EmailField()
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    rol = serializers.CharField(read_only=True)
    activo = serializers.BooleanField(default=True)
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)


class AdministradorSerializer(UsuarioSerializer):
    """Serializer para Administrador"""
    pass


class AdministradorCreateSerializer(serializers.Serializer):
    """Serializer para crear Administrador"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)


class AlumnoSerializer(UsuarioSerializer):
    """Serializer para Alumno"""
    grupo_id = ObjectIdField()
    grupo_nombre = serializers.CharField(max_length=1, read_only=True)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado']
    )


class AlumnoCreateSerializer(serializers.Serializer):
    """Serializer para crear Alumno"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    grupo_id = ObjectIdField()
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        default='Básico'
    )


class AlumnoUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar Alumno"""
    nombre = serializers.CharField(max_length=100, required=False)
    apellido = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    grupo_id = ObjectIdField(required=False)
    nivel = serializers.ChoiceField(
        choices=['Básico', 'Intermedio', 'Avanzado'],
        required=False
    )
    activo = serializers.BooleanField(required=False)


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
