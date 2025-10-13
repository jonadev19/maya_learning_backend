from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import Tema, Material, Vocabulario
from .serializers import (
    TemaSerializer,
    TemaCreateSerializer,
    MaterialSerializer,
    MaterialCreateSerializer,
    VocabularioSerializer,
    VocabularioCreateSerializer
)
from usuarios.permissions import IsAdminOrReadOnly


class TemaListView(APIView):
    """
    GET /api/temas/ - Lista todos los temas
    POST /api/temas/ - Crea un nuevo tema
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        temas = Tema.listar_activos()
        serializer = TemaSerializer(temas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemaCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            tema_id = Tema.crear(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data.get('descripcion', ''),
                orden=serializer.validated_data.get('orden', 0)
            )
            tema = Tema.find_one({'_id': tema_id})
            response_serializer = TemaSerializer(tema)
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


class TemaDetailView(APIView):
    """GET /api/temas/<id>/ - Detalle de un tema"""
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            tema = Tema.find_one({'_id': ObjectId(id)})
            if not tema:
                return Response(
                    {'error': 'Tema no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = TemaSerializer(tema)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MaterialListView(APIView):
    """
    GET /api/materiales/ - Lista todos los materiales
    POST /api/materiales/ - Crea un nuevo material
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # Filtros opcionales
        tema_id = request.query_params.get('tema_id', None)
        nivel = request.query_params.get('nivel', None)

        if tema_id and nivel:
            materiales = Material.listar_por_tema_y_nivel(tema_id, nivel)
        elif tema_id:
            materiales = Material.listar_por_tema(tema_id)
        elif nivel:
            materiales = Material.listar_por_nivel(nivel)
        else:
            materiales = Material.find({'activo': True})

        serializer = MaterialSerializer(materiales, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaterialCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            material_id = Material.crear(
                tema_id=serializer.validated_data['tema_id'],
                nivel=serializer.validated_data['nivel'],
                titulo=serializer.validated_data['titulo'],
                contenido=serializer.validated_data['contenido'],
                recursos=serializer.validated_data.get('recursos', []),
                orden=serializer.validated_data.get('orden', 0)
            )
            material = Material.obtener_por_id(material_id)
            response_serializer = MaterialSerializer(material)
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


class MaterialDetailView(APIView):
    """GET /api/materiales/<id>/ - Detalle de un material"""
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            material = Material.obtener_por_id(id)
            if not material:
                return Response(
                    {'error': 'Material no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = MaterialSerializer(material)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VocabularioListView(APIView):
    """
    GET /api/vocabulario/ - Lista palabras del vocabulario
    POST /api/vocabulario/ - Crea una nueva palabra del vocabulario
    """
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # Filtros opcionales
        tema_id = request.query_params.get('tema_id', None)
        nivel = request.query_params.get('nivel', None)
        buscar = request.query_params.get('buscar', None)

        if buscar:
            vocabulario = Vocabulario.buscar_palabra(buscar)
        elif tema_id and nivel:
            vocabulario = Vocabulario.listar_por_tema_y_nivel(tema_id, nivel)
        elif tema_id:
            vocabulario = Vocabulario.listar_por_tema(tema_id)
        else:
            vocabulario = Vocabulario.find({'activo': True})

        serializer = VocabularioSerializer(vocabulario, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VocabularioCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            vocabulario_id = Vocabulario.crear(
                tema_id=serializer.validated_data['tema_id'],
                palabra_maya=serializer.validated_data['palabra_maya'],
                palabra_espanol=serializer.validated_data['palabra_espanol'],
                pronunciacion=serializer.validated_data.get('pronunciacion', ''),
                imagen_url=serializer.validated_data.get('imagen_url', ''),
                audio_url=serializer.validated_data.get('audio_url', ''),
                nivel=serializer.validated_data.get('nivel', 'Básico')
            )
            palabra = Vocabulario.obtener_por_id(vocabulario_id)
            response_serializer = VocabularioSerializer(palabra)
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


class VocabularioDetailView(APIView):
    """GET /api/vocabulario/<id>/ - Detalle de una palabra"""
    authentication_classes = []
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            palabra = Vocabulario.obtener_por_id(id)
            if not palabra:
                return Response(
                    {'error': 'Palabra no encontrada'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = VocabularioSerializer(palabra)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
