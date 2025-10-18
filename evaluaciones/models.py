from django.conf import settings
from bson import ObjectId
from datetime import datetime
from usuarios.models import MongoDBModel, Alumno
from contenido.models import Tema


class Actividad(MongoDBModel):
    """Modelo para Actividades/Ejercicios que los alumnos deben completar"""
    collection_name = 'actividades'

    NIVELES = ['Básico', 'Intermedio', 'Avanzado']
    TIPOS = ['opcion_multiple', 'emparejar', 'completar', 'escribir']

    @classmethod
    def crear(cls, tema_id, nivel, titulo, descripcion, tipo='opcion_multiple',
              duracion_minutos=None, orden=0):
        """Crea una nueva actividad"""
        if nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        if tipo not in cls.TIPOS:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(cls.TIPOS)}")

        # Verificar que el tema existe
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        tema = Tema.find_one({'_id': tema_id})
        if not tema:
            raise ValueError("El tema especificado no existe")

        data = {
            'tema_id': tema_id,
            'tema_nombre': tema['nombre'],
            'nivel': nivel,
            'titulo': titulo,
            'descripcion': descripcion,
            'tipo': tipo,
            'duracion_minutos': duracion_minutos,
            'orden': orden,
            'preguntas': [],  # Array de preguntas
            'puntaje_total': 0,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_id(cls, actividad_id):
        """Obtiene una actividad por ID"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)
        return cls.find_one({'_id': actividad_id})

    @classmethod
    def listar_por_tema(cls, tema_id):
        """Lista actividades por tema"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)
        return cls.find({'tema_id': tema_id, 'activo': True}, sort=[('orden', 1)])

    @classmethod
    def listar_por_tema_y_nivel(cls, tema_id, nivel):
        """Lista actividades por tema y nivel"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        if nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        return cls.find({
            'tema_id': tema_id,
            'nivel': nivel,
            'activo': True
        }, sort=[('orden', 1)])

    @classmethod
    def agregar_pregunta(cls, actividad_id, pregunta_texto, respuesta_correcta,
                        opciones=None, puntos=1, tipo='opcion_multiple'):
        """Agrega una pregunta a la actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        actividad = cls.find_one({'_id': actividad_id})
        if not actividad:
            raise ValueError("La actividad especificada no existe")

        if opciones is None:
            opciones = []

        pregunta = {
            'id': str(ObjectId()),  # ID único para la pregunta
            'texto': pregunta_texto,
            'tipo': tipo,
            'opciones': opciones,  # Lista de opciones posibles
            'respuesta_correcta': respuesta_correcta,
            'puntos': puntos,
            'orden': len(actividad.get('preguntas', []))
        }

        # Agregar pregunta y actualizar puntaje total
        nuevo_puntaje = actividad.get('puntaje_total', 0) + puntos

        return cls.get_collection().update_one(
            {'_id': actividad_id},
            {
                '$push': {'preguntas': pregunta},
                '$set': {
                    'puntaje_total': nuevo_puntaje,
                    'actualizado_en': datetime.utcnow()
                }
            }
        )

    @classmethod
    def actualizar_pregunta(cls, actividad_id, pregunta_id, datos):
        """Actualiza una pregunta específica de la actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        # Actualizar la pregunta en el array
        return cls.get_collection().update_one(
            {'_id': actividad_id, 'preguntas.id': pregunta_id},
            {
                '$set': {
                    'preguntas.$': {**datos, 'id': pregunta_id},
                    'actualizado_en': datetime.utcnow()
                }
            }
        )

    @classmethod
    def eliminar_pregunta(cls, actividad_id, pregunta_id):
        """Elimina una pregunta de la actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        return cls.get_collection().update_one(
            {'_id': actividad_id},
            {
                '$pull': {'preguntas': {'id': pregunta_id}},
                '$set': {'actualizado_en': datetime.utcnow()}
            }
        )

    @classmethod
    def actualizar(cls, actividad_id, datos):
        """Actualiza una actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        # Si se actualiza el nivel, validar
        if 'nivel' in datos and datos['nivel'] not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        # Si se actualiza el tipo, validar
        if 'tipo' in datos and datos['tipo'] not in cls.TIPOS:
            raise ValueError(f"Tipo debe ser uno de: {', '.join(cls.TIPOS)}")

        # Si se actualiza el tema_id, validar que existe y actualizar tema_nombre
        if 'tema_id' in datos:
            tema_id = datos['tema_id']
            if isinstance(tema_id, str):
                tema_id = ObjectId(tema_id)
            tema = Tema.find_one({'_id': tema_id})
            if not tema:
                raise ValueError("El tema especificado no existe")
            datos['tema_nombre'] = tema['nombre']

        return cls.update_one({'_id': actividad_id}, datos)


class IntentoPrueba(MongoDBModel):
    """Modelo para registrar cuando un alumno intenta una actividad"""
    collection_name = 'intentos_prueba'

    ESTADOS = ['en_progreso', 'completada', 'abandonada']

    @classmethod
    def crear(cls, alumno_id, actividad_id):
        """Crea un nuevo intento de prueba"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        # Verificar que el alumno existe
        alumno = Alumno.obtener_por_id(alumno_id)
        if not alumno:
            raise ValueError("El alumno especificado no existe")

        # Verificar que la actividad existe
        actividad = Actividad.obtener_por_id(actividad_id)
        if not actividad:
            raise ValueError("La actividad especificada no existe")

        data = {
            'alumno_id': alumno_id,
            'alumno_nombre': f"{alumno['nombre']} {alumno['apellido']}",
            'alumno_email': alumno['email'],
            'grupo_nombre': alumno.get('grupo_nombre', ''),
            'actividad_id': actividad_id,
            'actividad_titulo': actividad['titulo'],
            'tema_nombre': actividad['tema_nombre'],
            'nivel': actividad['nivel'],
            'fecha_inicio': datetime.utcnow(),
            'fecha_finalizacion': None,
            'estado': 'en_progreso',
            'respuestas': [],  # Array de respuestas
            'puntaje_obtenido': 0,
            'puntaje_total': actividad['puntaje_total']
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_id(cls, intento_id):
        """Obtiene un intento por ID"""
        if isinstance(intento_id, str):
            intento_id = ObjectId(intento_id)
        return cls.find_one({'_id': intento_id})

    @classmethod
    def listar_por_alumno(cls, alumno_id):
        """Lista todos los intentos de un alumno"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        return cls.find({'alumno_id': alumno_id}, sort=[('fecha_inicio', -1)])

    @classmethod
    def listar_por_actividad(cls, actividad_id):
        """Lista todos los intentos de una actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)
        return cls.find({'actividad_id': actividad_id}, sort=[('fecha_inicio', -1)])

    @classmethod
    def obtener_intento_activo(cls, alumno_id, actividad_id):
        """Obtiene el intento activo de un alumno en una actividad"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)

        return cls.find_one({
            'alumno_id': alumno_id,
            'actividad_id': actividad_id,
            'estado': 'en_progreso'
        })

    @classmethod
    def registrar_respuesta(cls, intento_id, pregunta_id, respuesta_alumno, es_correcta, puntos_obtenidos):
        """Registra una respuesta del alumno"""
        if isinstance(intento_id, str):
            intento_id = ObjectId(intento_id)

        intento = cls.find_one({'_id': intento_id})
        if not intento:
            raise ValueError("El intento especificado no existe")

        respuesta = {
            'pregunta_id': pregunta_id,
            'respuesta_alumno': respuesta_alumno,
            'es_correcta': es_correcta,
            'puntos_obtenidos': puntos_obtenidos,
            'fecha_respuesta': datetime.utcnow()
        }

        # Agregar respuesta y actualizar puntaje
        nuevo_puntaje = intento.get('puntaje_obtenido', 0) + puntos_obtenidos

        return cls.get_collection().update_one(
            {'_id': intento_id},
            {
                '$push': {'respuestas': respuesta},
                '$set': {
                    'puntaje_obtenido': nuevo_puntaje,
                    'actualizado_en': datetime.utcnow()
                }
            }
        )

    @classmethod
    def finalizar_intento(cls, intento_id):
        """Marca el intento como completado"""
        if isinstance(intento_id, str):
            intento_id = ObjectId(intento_id)

        return cls.update_one(
            {'_id': intento_id},
            {
                'estado': 'completada',
                'fecha_finalizacion': datetime.utcnow()
            }
        )


class Calificacion(MongoDBModel):
    """Modelo para Calificaciones finales de los alumnos"""
    collection_name = 'calificaciones'

    @classmethod
    def crear_desde_intento(cls, intento_id):
        """Crea una calificación a partir de un intento completado"""
        if isinstance(intento_id, str):
            intento_id = ObjectId(intento_id)

        intento = IntentoPrueba.obtener_por_id(intento_id)
        if not intento:
            raise ValueError("El intento especificado no existe")

        if intento['estado'] != 'completada':
            raise ValueError("El intento debe estar completado para generar una calificación")

        # Calcular porcentaje
        puntaje_total = intento['puntaje_total']
        puntaje_obtenido = intento['puntaje_obtenido']
        porcentaje = (puntaje_obtenido / puntaje_total * 100) if puntaje_total > 0 else 0

        # Determinar si aprobó (>= 70%)
        aprobado = porcentaje >= 70

        data = {
            'alumno_id': intento['alumno_id'],
            'alumno_nombre': intento['alumno_nombre'],
            'alumno_email': intento['alumno_email'],
            'grupo_nombre': intento['grupo_nombre'],
            'actividad_id': intento['actividad_id'],
            'actividad_titulo': intento['actividad_titulo'],
            'tema_nombre': intento['tema_nombre'],
            'nivel': intento['nivel'],
            'intento_id': intento_id,
            'puntaje_obtenido': puntaje_obtenido,
            'puntaje_total': puntaje_total,
            'porcentaje': round(porcentaje, 2),
            'aprobado': aprobado,
            'fecha_evaluacion': intento['fecha_finalizacion'],
            'duracion_minutos': cls._calcular_duracion(intento['fecha_inicio'], intento['fecha_finalizacion'])
        }
        return cls.insert_one(data)

    @classmethod
    def _calcular_duracion(cls, fecha_inicio, fecha_fin):
        """Calcula la duración en minutos"""
        if fecha_inicio and fecha_fin:
            delta = fecha_fin - fecha_inicio
            return round(delta.total_seconds() / 60, 2)
        return 0

    @classmethod
    def obtener_por_id(cls, calificacion_id):
        """Obtiene una calificación por ID"""
        if isinstance(calificacion_id, str):
            calificacion_id = ObjectId(calificacion_id)
        return cls.find_one({'_id': calificacion_id})

    @classmethod
    def listar_por_alumno(cls, alumno_id):
        """Lista todas las calificaciones de un alumno"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        return cls.find({'alumno_id': alumno_id}, sort=[('fecha_evaluacion', -1)])

    @classmethod
    def listar_por_grupo(cls, grupo_nombre):
        """Lista todas las calificaciones de un grupo"""
        return cls.find({'grupo_nombre': grupo_nombre}, sort=[('fecha_evaluacion', -1)])

    @classmethod
    def listar_por_tema(cls, tema_nombre):
        """Lista todas las calificaciones de un tema"""
        return cls.find({'tema_nombre': tema_nombre}, sort=[('fecha_evaluacion', -1)])

    @classmethod
    def listar_por_actividad(cls, actividad_id):
        """Lista todas las calificaciones de una actividad"""
        if isinstance(actividad_id, str):
            actividad_id = ObjectId(actividad_id)
        return cls.find({'actividad_id': actividad_id}, sort=[('fecha_evaluacion', -1)])

    @classmethod
    def obtener_promedio_alumno(cls, alumno_id, tema_nombre=None):
        """Obtiene el promedio de calificaciones de un alumno"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)

        query = {'alumno_id': alumno_id}
        if tema_nombre:
            query['tema_nombre'] = tema_nombre

        calificaciones = cls.find(query)

        if not calificaciones:
            return 0

        total = sum(cal['porcentaje'] for cal in calificaciones)
        return round(total / len(calificaciones), 2)

    @classmethod
    def obtener_promedio_grupo(cls, grupo_nombre, tema_nombre=None):
        """Obtiene el promedio de calificaciones de un grupo"""
        query = {'grupo_nombre': grupo_nombre}
        if tema_nombre:
            query['tema_nombre'] = tema_nombre

        calificaciones = cls.find(query)

        if not calificaciones:
            return 0

        total = sum(cal['porcentaje'] for cal in calificaciones)
        return round(total / len(calificaciones), 2)

    @classmethod
    def obtener_estadisticas_tema(cls, tema_nombre, grupo_nombre=None):
        """Obtiene estadísticas de un tema"""
        query = {'tema_nombre': tema_nombre}
        if grupo_nombre:
            query['grupo_nombre'] = grupo_nombre

        calificaciones = cls.find(query)

        if not calificaciones:
            return {
                'total_evaluaciones': 0,
                'promedio': 0,
                'aprobados': 0,
                'reprobados': 0,
                'porcentaje_aprobacion': 0
            }

        total = len(calificaciones)
        aprobados = sum(1 for cal in calificaciones if cal['aprobado'])
        reprobados = total - aprobados
        promedio = sum(cal['porcentaje'] for cal in calificaciones) / total

        return {
            'total_evaluaciones': total,
            'promedio': round(promedio, 2),
            'aprobados': aprobados,
            'reprobados': reprobados,
            'porcentaje_aprobacion': round((aprobados / total * 100), 2)
        }
