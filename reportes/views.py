from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId

from .models import ReporteGenerado
from .serializers import ReporteGeneradoSerializer


class ReporteListView(APIView):
    """GET /api/reportes/ - Lista todos los reportes generados"""

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


class ReporteDetailView(APIView):
    """GET /api/reportes/<id>/ - Detalle de un reporte"""

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
