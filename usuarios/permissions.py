from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class IsAdmin(BasePermission):
    """
    Permiso que solo permite acceso a administradores
    """
    message = 'Solo los administradores tienen acceso a este recurso'

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False

        try:
            # Extraer y decodificar el token
            token_string = auth_header.split(' ')[1]
            token = AccessToken(token_string)

            # Verificar el rol en el token
            rol = token.get('rol', '')
            return rol == 'administrador'

        except (TokenError, IndexError):
            return False


class IsAlumno(BasePermission):
    """
    Permiso que solo permite acceso a alumnos
    """
    message = 'Solo los alumnos tienen acceso a este recurso'

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False

        try:
            # Extraer y decodificar el token
            token_string = auth_header.split(' ')[1]
            token = AccessToken(token_string)

            # Verificar el rol en el token
            rol = token.get('rol', '')
            return rol == 'alumno'

        except (TokenError, IndexError):
            return False


class IsAdminOrReadOnly(BasePermission):
    """
    Permiso que permite lectura a todos los autenticados,
    pero solo escritura a administradores
    """
    message = 'Solo los administradores pueden modificar este recurso'

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False

        try:
            # Extraer y decodificar el token
            token_string = auth_header.split(' ')[1]
            token = AccessToken(token_string)

            # Permitir lectura a todos los autenticados
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True

            # Solo administradores pueden escribir/modificar
            rol = token.get('rol', '')
            return rol == 'administrador'

        except (TokenError, IndexError):
            return False


class IsOwnerOrAdmin(BasePermission):
    """
    Permiso que permite acceso al propietario del recurso o a administradores
    """
    message = 'Solo el propietario o un administrador pueden acceder a este recurso'

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False

        try:
            # Extraer y decodificar el token
            token_string = auth_header.split(' ')[1]
            token = AccessToken(token_string)

            # Guardar el user_id y rol en el request para uso posterior
            request.user_id = token.get('user_id')
            request.user_rol = token.get('rol', '')

            return True

        except (TokenError, IndexError):
            return False

    def has_object_permission(self, request, view, obj):
        """
        Verifica si el usuario es el propietario del objeto o es administrador
        """
        # Si es administrador, tiene acceso total
        if request.user_rol == 'administrador':
            return True

        # Verificar si el usuario es el propietario
        # obj puede ser un dict (MongoDB) o un objeto
        if isinstance(obj, dict):
            obj_user_id = str(obj.get('_id'))
        else:
            obj_user_id = str(getattr(obj, '_id', None))

        return str(request.user_id) == obj_user_id


class IsAuthenticated(BasePermission):
    """
    Permiso que verifica si el usuario está autenticado mediante JWT
    Sin intentar buscar el usuario en la base de datos de Django
    """
    message = 'Se requiere autenticación'

    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return False

        try:
            # Extraer y decodificar el token
            token_string = auth_header.split(' ')[1]
            token = AccessToken(token_string)

            # Guardar información del usuario en el request
            request.user_id = token.get('user_id')
            request.user_email = token.get('email')
            request.user_rol = token.get('rol', '')
            request.user_nombre = token.get('nombre', '')
            request.user_apellido = token.get('apellido', '')

            return True

        except (TokenError, IndexError):
            return False