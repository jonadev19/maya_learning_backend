from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import Usuario
from .serializers import LoginSerializer
from .permissions import IsAuthenticated


class LoginView(APIView):
    """
    Vista de login que autentica usuarios y retorna tokens JWT

    POST /api/auth/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Autenticar usando el modelo de Usuario de MongoDB
        usuario = Usuario.autenticar(email, password)

        if not usuario:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Crear tokens JWT manualmente
        # Como usamos MongoDB, necesitamos crear el token con los datos del usuario
        refresh = RefreshToken()

        # Agregar claims personalizados al token
        refresh['user_id'] = str(usuario['_id'])
        refresh['email'] = usuario['email']
        refresh['rol'] = usuario['rol']
        refresh['nombre'] = usuario['nombre']
        refresh['apellido'] = usuario['apellido']

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(usuario['_id']),
                'email': usuario['email'],
                'nombre': usuario['nombre'],
                'apellido': usuario['apellido'],
                'rol': usuario['rol']
            }
        }, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Vista personalizada para refrescar tokens JWT

    POST /api/auth/refresh/
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response({
                'access': response.data.get('access'),
                'refresh': response.data.get('refresh')
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {'error': 'Token inválido o expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """
    Vista de logout que invalida el refresh token

    POST /api/auth/logout/
    """
    authentication_classes = []  # Deshabilitar autenticación automática de DRF
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {'message': 'Sesión cerrada exitosamente'},
                status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {'error': 'Token inválido o expirado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MeView(APIView):
    """
    Vista para obtener información del usuario autenticado

    GET /api/auth/me/
    """
    authentication_classes = []  # Deshabilitar autenticación automática de DRF
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # El permiso IsAuthenticated ya extrajo la info del token
            # y la guardó en request.user_id, request.user_email, etc.
            user_id = getattr(request, 'user_id', None)

            if not user_id:
                return Response(
                    {'error': 'Token no proporcionado'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Buscar el usuario en MongoDB para obtener datos actualizados
            usuario = Usuario.obtener_por_id(user_id)

            if not usuario:
                return Response(
                    {'error': 'Usuario no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                'id': str(usuario['_id']),
                'email': usuario['email'],
                'nombre': usuario['nombre'],
                'apellido': usuario['apellido'],
                'rol': usuario['rol'],
                'activo': usuario.get('activo', True)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )