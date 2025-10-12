from django.conf import settings
from bson import ObjectId
from datetime import datetime
from usuarios.models import MongoDBModel


class ReporteGenerado(MongoDBModel):
    """Modelo para registrar el historial de reportes PDF generados"""
    collection_name = 'reportes_generados'

    TIPOS_REPORTE = ['individual', 'grupo', 'tema', 'general']

    @classmethod
    def crear(cls, tipo, generado_por_id, titulo, descripcion='',
              alumno_id=None, grupo_nombre=None, tema_nombre=None,
              archivo_url='', metadatos=None):
        """Crea un registro de reporte generado"""
        if tipo not in cls.TIPOS_REPORTE:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(cls.TIPOS_REPORTE)}")

        if metadatos is None:
            metadatos = {}

        data = {
            'tipo': tipo,
            'generado_por_id': ObjectId(generado_por_id) if isinstance(generado_por_id, str) else generado_por_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'alumno_id': ObjectId(alumno_id) if isinstance(alumno_id, str) and alumno_id else alumno_id,
            'grupo_nombre': grupo_nombre,
            'tema_nombre': tema_nombre,
            'archivo_url': archivo_url,
            'metadatos': metadatos,  # Datos extra como fecha_inicio, fecha_fin, etc.
            'fecha_generacion': datetime.utcnow()
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_id(cls, reporte_id):
        """Obtiene un reporte por ID"""
        if isinstance(reporte_id, str):
            reporte_id = ObjectId(reporte_id)
        return cls.find_one({'_id': reporte_id})

    @classmethod
    def listar_por_tipo(cls, tipo):
        """Lista reportes por tipo"""
        if tipo not in cls.TIPOS_REPORTE:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(cls.TIPOS_REPORTE)}")
        return cls.find({'tipo': tipo}, sort=[('fecha_generacion', -1)])

    @classmethod
    def listar_por_generador(cls, generado_por_id):
        """Lista todos los reportes generados por un administrador"""
        if isinstance(generado_por_id, str):
            generado_por_id = ObjectId(generado_por_id)
        return cls.find({'generado_por_id': generado_por_id}, sort=[('fecha_generacion', -1)])

    @classmethod
    def listar_por_alumno(cls, alumno_id):
        """Lista todos los reportes de un alumno"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        return cls.find({'alumno_id': alumno_id}, sort=[('fecha_generacion', -1)])

    @classmethod
    def listar_por_grupo(cls, grupo_nombre):
        """Lista todos los reportes de un grupo"""
        return cls.find({'grupo_nombre': grupo_nombre}, sort=[('fecha_generacion', -1)])

    @classmethod
    def listar_recientes(cls, limite=10):
        """Lista los reportes más recientes"""
        return cls.find({}, sort=[('fecha_generacion', -1)], limit=limite)
