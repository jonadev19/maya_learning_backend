from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import Tema, Material, Vocabulario
from .serializers import TemaSerializer, MaterialSerializer, VocabularioSerializer


class TemaListView(APIView):
    """GET /api/temas/ - Lista todos los temas"""

    def get(self, request):
        temas = Tema.listar_activos()
        serializer = TemaSerializer(temas, many=True)
        return Response(serializer.data)


class TemaDetailView(APIView):
    """GET /api/temas/<id>/ - Detalle de un tema"""

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
    """GET /api/materiales/ - Lista todos los materiales"""

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


class MaterialDetailView(APIView):
    """GET /api/materiales/<id>/ - Detalle de un material"""

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
    """GET /api/vocabulario/ - Lista palabras del vocabulario"""

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


class VocabularioDetailView(APIView):
    """GET /api/vocabulario/<id>/ - Detalle de una palabra"""

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
