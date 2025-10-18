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
    """
    GET /api/reportes/<id>/ - Detalle de un reporte
    PUT /api/reportes/<id>/ - Actualiza un reporte
    DELETE /api/reportes/<id>/ - Elimina un reporte permanentemente
    """
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

    def put(self, request, id):
        try:
            reporte = ReporteGenerado.obtener_por_id(id)
            if not reporte:
                return Response(
                    {'error': 'Reporte no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Datos que se pueden actualizar
            datos_actualizacion = {}
            if 'tipo' in request.data:
                datos_actualizacion['tipo'] = request.data['tipo']
            if 'titulo' in request.data:
                datos_actualizacion['titulo'] = request.data['titulo']
            if 'descripcion' in request.data:
                datos_actualizacion['descripcion'] = request.data['descripcion']
            if 'archivo_url' in request.data:
                datos_actualizacion['archivo_url'] = request.data['archivo_url']
            if 'metadatos' in request.data:
                datos_actualizacion['metadatos'] = request.data['metadatos']
            if 'alumno_id' in request.data:
                datos_actualizacion['alumno_id'] = request.data['alumno_id']
            if 'grupo_nombre' in request.data:
                datos_actualizacion['grupo_nombre'] = request.data['grupo_nombre']
            if 'tema_nombre' in request.data:
                datos_actualizacion['tema_nombre'] = request.data['tema_nombre']

            # Actualizar el reporte
            ReporteGenerado.actualizar(id, datos_actualizacion)

            # Retornar el reporte actualizado
            reporte_actualizado = ReporteGenerado.obtener_por_id(id)
            serializer = ReporteGeneradoSerializer(reporte_actualizado)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            reporte = ReporteGenerado.obtener_por_id(id)
            if not reporte:
                return Response(
                    {'error': 'Reporte no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Hard delete - eliminar permanentemente
            ReporteGenerado.delete_one({'_id': ObjectId(id)})

            return Response(
                {'message': 'Reporte eliminado permanentemente'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
