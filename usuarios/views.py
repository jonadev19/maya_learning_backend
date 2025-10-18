from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from bson import ObjectId

from .models import Grupo, Administrador, Alumno, Usuario
from .serializers import (
    GrupoSerializer,
    AdministradorSerializer,
    AdministradorCreateSerializer,
    AlumnoSerializer,
    AlumnoCreateSerializer,
    UsuarioSerializer
)
from .permissions import IsAdmin, IsAdminOrReadOnly


class GrupoListView(APIView):
    """
    GET /api/grupos/ - Lista todos los grupos
    POST /api/grupos/ - Crea un nuevo grupo
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        grupos = Grupo.listar_activos()
        serializer = GrupoSerializer(grupos, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            nombre = request.data.get('nombre')
            descripcion = request.data.get('descripcion', '')

            if not nombre:
                return Response(
                    {'error': 'El nombre del grupo es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            grupo_id = Grupo.crear(nombre, descripcion)
            grupo = Grupo.find_one({'_id': grupo_id})
            serializer = GrupoSerializer(grupo)
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


class GrupoDetailView(APIView):
    """
    GET /api/grupos/<id>/ - Detalle de un grupo
    PUT /api/grupos/<id>/ - Actualiza un grupo
    DELETE /api/grupos/<id>/ - Elimina un grupo (soft delete)
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            grupo = Grupo.find_one({'_id': ObjectId(id)})
            if not grupo:
                return Response(
                    {'error': 'Grupo no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = GrupoSerializer(grupo)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, id):
        try:
            grupo = Grupo.find_one({'_id': ObjectId(id)})
            if not grupo:
                return Response(
                    {'error': 'Grupo no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Datos que se pueden actualizar
            datos_actualizacion = {}
            if 'descripcion' in request.data:
                datos_actualizacion['descripcion'] = request.data['descripcion']
            if 'activo' in request.data:
                datos_actualizacion['activo'] = request.data['activo']

            # Actualizar el grupo
            Grupo.update_one({'_id': ObjectId(id)}, datos_actualizacion)

            # Retornar el grupo actualizado
            grupo_actualizado = Grupo.find_one({'_id': ObjectId(id)})
            serializer = GrupoSerializer(grupo_actualizado)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            grupo = Grupo.find_one({'_id': ObjectId(id)})
            if not grupo:
                return Response(
                    {'error': 'Grupo no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Soft delete - marcar como inactivo
            Grupo.update_one({'_id': ObjectId(id)}, {'activo': False})

            return Response(
                {'message': 'Grupo eliminado exitosamente'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AdministradorListView(APIView):
    """
    GET /api/administradores/ - Lista todos los administradores
    POST /api/administradores/ - Crea un nuevo administrador
    """
    authentication_classes = []
    permission_classes = [IsAdmin]

    def get(self, request):
        admins = Administrador.listar_todos()
        serializer = AdministradorSerializer(admins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdministradorCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin_id = Administrador.crear_admin(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                nombre=serializer.validated_data['nombre'],
                apellido=serializer.validated_data['apellido']
            )
            admin = Administrador.obtener_por_id(admin_id)
            response_serializer = AdministradorSerializer(admin)
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


class AdministradorDetailView(APIView):
    """
    GET /api/administradores/<id>/ - Detalle de un administrador
    PUT /api/administradores/<id>/ - Actualiza un administrador
    DELETE /api/administradores/<id>/ - Elimina un administrador (soft delete)
    """
    authentication_classes = []
    permission_classes = [IsAdmin]

    def get(self, request, id):
        try:
            admin = Administrador.obtener_por_id(id)
            if not admin:
                return Response(
                    {'error': 'Administrador no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AdministradorSerializer(admin)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, id):
        try:
            admin = Administrador.obtener_por_id(id)
            if not admin:
                return Response(
                    {'error': 'Administrador no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Datos que se pueden actualizar
            datos_actualizacion = {}
            if 'nombre' in request.data:
                datos_actualizacion['nombre'] = request.data['nombre']
            if 'apellido' in request.data:
                datos_actualizacion['apellido'] = request.data['apellido']
            if 'email' in request.data:
                # Verificar que el email no esté en uso por otro usuario
                email_existente = Usuario.find_one({'email': request.data['email']})
                if email_existente and str(email_existente['_id']) != str(id):
                    return Response(
                        {'error': 'El email ya está en uso'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                datos_actualizacion['email'] = request.data['email']
            if 'activo' in request.data:
                datos_actualizacion['activo'] = request.data['activo']
            if 'password' in request.data:
                from django.contrib.auth.hashers import make_password
                datos_actualizacion['password'] = make_password(request.data['password'])

            # Actualizar el administrador
            Administrador.update_one({'_id': ObjectId(id)}, datos_actualizacion)

            # Retornar el administrador actualizado
            admin_actualizado = Administrador.obtener_por_id(id)
            serializer = AdministradorSerializer(admin_actualizado)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            admin = Administrador.obtener_por_id(id)
            if not admin:
                return Response(
                    {'error': 'Administrador no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Soft delete - marcar como inactivo
            Administrador.update_one({'_id': ObjectId(id)}, {'activo': False})

            return Response(
                {'message': 'Administrador eliminado exitosamente'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AlumnoListView(APIView):
    """
    GET /api/alumnos/ - Lista todos los alumnos
    POST /api/alumnos/ - Crea un nuevo alumno
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # Filtros opcionales via query params
        grupo = request.query_params.get('grupo', None)
        nivel = request.query_params.get('nivel', None)

        if grupo:
            alumnos = Alumno.listar_por_grupo(grupo)
        elif nivel:
            alumnos = Alumno.listar_por_nivel(nivel)
        else:
            alumnos = Alumno.listar_todos()

        serializer = AlumnoSerializer(alumnos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlumnoCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            alumno_id = Alumno.crear_alumno(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                nombre=serializer.validated_data['nombre'],
                apellido=serializer.validated_data['apellido'],
                grupo_id=serializer.validated_data['grupo_id'],
                nivel=serializer.validated_data.get('nivel', 'Básico')
            )
            alumno = Alumno.obtener_por_id(alumno_id)
            response_serializer = AlumnoSerializer(alumno)
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


class AlumnoDetailView(APIView):
    """
    GET /api/alumnos/<id>/ - Detalle de un alumno
    PUT /api/alumnos/<id>/ - Actualiza un alumno
    DELETE /api/alumnos/<id>/ - Elimina un alumno (soft delete)
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            alumno = Alumno.obtener_por_id(id)
            if not alumno:
                return Response(
                    {'error': 'Alumno no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = AlumnoSerializer(alumno)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, id):
        try:
            alumno = Alumno.obtener_por_id(id)
            if not alumno:
                return Response(
                    {'error': 'Alumno no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Datos que se pueden actualizar
            datos_actualizacion = {}
            if 'nombre' in request.data:
                datos_actualizacion['nombre'] = request.data['nombre']
            if 'apellido' in request.data:
                datos_actualizacion['apellido'] = request.data['apellido']
            if 'email' in request.data:
                # Verificar que el email no esté en uso por otro usuario
                email_existente = Usuario.find_one({'email': request.data['email']})
                if email_existente and str(email_existente['_id']) != str(id):
                    return Response(
                        {'error': 'El email ya está en uso'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                datos_actualizacion['email'] = request.data['email']
            if 'activo' in request.data:
                datos_actualizacion['activo'] = request.data['activo']
            if 'password' in request.data:
                from django.contrib.auth.hashers import make_password
                datos_actualizacion['password'] = make_password(request.data['password'])
            if 'nivel' in request.data:
                if request.data['nivel'] not in Alumno.NIVELES:
                    return Response(
                        {'error': f"Nivel debe ser uno de: {', '.join(Alumno.NIVELES)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                datos_actualizacion['nivel'] = request.data['nivel']
            if 'grupo_id' in request.data:
                grupo_id = request.data['grupo_id']
                if isinstance(grupo_id, str):
                    grupo_id = ObjectId(grupo_id)
                grupo = Grupo.find_one({'_id': grupo_id})
                if not grupo:
                    return Response(
                        {'error': 'El grupo especificado no existe'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                datos_actualizacion['grupo_id'] = grupo_id
                datos_actualizacion['grupo_nombre'] = grupo['nombre']

            # Actualizar el alumno
            Alumno.update_one({'_id': ObjectId(id)}, datos_actualizacion)

            # Retornar el alumno actualizado
            alumno_actualizado = Alumno.obtener_por_id(id)
            serializer = AlumnoSerializer(alumno_actualizado)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            alumno = Alumno.obtener_por_id(id)
            if not alumno:
                return Response(
                    {'error': 'Alumno no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Soft delete - marcar como inactivo
            Alumno.update_one({'_id': ObjectId(id)}, {'activo': False})

            return Response(
                {'message': 'Alumno eliminado exitosamente'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UsuarioListView(APIView):
    """GET /api/usuarios/ - Lista todos los usuarios"""
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # Filtro opcional por rol
        rol = request.query_params.get('rol', None)

        if rol:
            usuarios = Usuario.listar_por_rol(rol)
        else:
            usuarios = Usuario.find({'activo': True})
            for usuario in usuarios:
                if 'password' in usuario:
                    del usuario['password']

        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class UsuarioDetailView(APIView):
    """GET /api/usuarios/<id>/ - Detalle de un usuario"""
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            usuario = Usuario.obtener_por_id(id)
            if not usuario:
                return Response(
                    {'error': 'Usuario no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
