from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import ReporteGenerado
from .serializers import ReporteGeneradoSerializer, ReporteGeneradoCreateSerializer
from usuarios.permissions import IsAuthenticated


class ReporteListView(APIView):
    """
    GET /api/reportes/ - Lista todos los reportes generados
    POST /api/reportes/ - Crea un nuevo registro de reporte
    """
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtros opcionales
        tipo = request.query_params.get('tipo', None)
        generado_por_id = request.query_params.get('generado_por', None)
        alumno_id = request.query_params.get('alumno_id', None)
        grupo_nombre = request.query_params.get('grupo', None)
        limite = request.query_params.get('limite', 10)

        try:
            limite = int(limite)
        except:
            limite = 10

        if tipo:
            reportes = ReporteGenerado.listar_por_tipo(tipo)
        elif generado_por_id:
            reportes = ReporteGenerado.listar_por_generador(generado_por_id)
        elif alumno_id:
            reportes = ReporteGenerado.listar_por_alumno(alumno_id)
        elif grupo_nombre:
            reportes = ReporteGenerado.listar_por_grupo(grupo_nombre)
        else:
            reportes = ReporteGenerado.listar_recientes(limite)

        serializer = ReporteGeneradoSerializer(reportes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReporteGeneradoCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            reporte_id = ReporteGenerado.crear(
                tipo=serializer.validated_data['tipo'],
                generado_por_id=serializer.validated_data['generado_por_id'],
                titulo=serializer.validated_data['titulo'],
                descripcion=serializer.validated_data.get('descripcion', ''),
                alumno_id=serializer.validated_data.get('alumno_id'),
                grupo_nombre=serializer.validated_data.get('grupo_nombre'),
                tema_nombre=serializer.validated_data.get('tema_nombre'),
                archivo_url=serializer.validated_data.get('archivo_url', ''),
                metadatos=serializer.validated_data.get('metadatos', {})
            )
            reporte = ReporteGenerado.obtener_por_id(reporte_id)
            response_serializer = ReporteGeneradoSerializer(reporte)
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


class ReporteDetailView(APIView):
    """GET /api/reportes/<id>/ - Detalle de un reporte"""
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            reporte = ReporteGenerado.obtener_por_id(id)
            if not reporte:
                return Response(
                    {'error': 'Reporte no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ReporteGeneradoSerializer(reporte)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
