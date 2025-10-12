from django.conf import settings
from bson import ObjectId
from datetime import datetime
from usuarios.models import MongoDBModel


class Tema(MongoDBModel):
    """Modelo para Temas de aprendizaje del lenguaje maya"""
    collection_name = 'temas'

    # Temas válidos según el enunciado
    TEMAS_VALIDOS = ['Números', 'Comidas', 'Objetos Cotidianos', 'Animales']

    @classmethod
    def crear(cls, nombre, descripcion='', orden=0):
        """Crea un nuevo tema"""
        if nombre not in cls.TEMAS_VALIDOS:
            raise ValueError(f"Tema debe ser uno de: {', '.join(cls.TEMAS_VALIDOS)}")

        # Verificar si ya existe
        existente = cls.find_one({'nombre': nombre})
        if existente:
            raise ValueError(f"El tema '{nombre}' ya existe")

        data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'orden': orden,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_nombre(cls, nombre):
        """Obtiene un tema por nombre"""
        return cls.find_one({'nombre': nombre})

    @classmethod
    def listar_activos(cls):
        """Lista todos los temas activos ordenados"""
        return cls.find({'activo': True}, sort=[('orden', 1)])

    @classmethod
    def actualizar(cls, tema_id, datos):
        """Actualiza un tema"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        # Si se actualiza el nombre, validar
        if 'nombre' in datos and datos['nombre'] not in cls.TEMAS_VALIDOS:
            raise ValueError(f"Tema debe ser uno de: {', '.join(cls.TEMAS_VALIDOS)}")

        return cls.update_one({'_id': tema_id}, datos)


class Material(MongoDBModel):
    """Modelo para Material educativo (información antes de cada actividad)"""
    collection_name = 'materiales'

    # Niveles válidos
    NIVELES = ['Básico', 'Intermedio', 'Avanzado']

    @classmethod
    def crear(cls, tema_id, nivel, titulo, contenido, recursos=None, orden=0):
        """Crea un nuevo material educativo"""
        if nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        # Verificar que el tema existe
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        tema = Tema.find_one({'_id': tema_id})
        if not tema:
            raise ValueError("El tema especificado no existe")

        if recursos is None:
            recursos = []

        data = {
            'tema_id': tema_id,
            'tema_nombre': tema['nombre'],
            'nivel': nivel,
            'titulo': titulo,
            'contenido': contenido,  # Texto explicativo del tema
            'recursos': recursos,  # URLs a imágenes, audios, videos
            'orden': orden,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_id(cls, material_id):
        """Obtiene un material por ID"""
        if isinstance(material_id, str):
            material_id = ObjectId(material_id)
        return cls.find_one({'_id': material_id})

    @classmethod
    def listar_por_tema(cls, tema_id):
        """Lista materiales por tema"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)
        return cls.find({'tema_id': tema_id, 'activo': True}, sort=[('orden', 1)])

    @classmethod
    def listar_por_tema_y_nivel(cls, tema_id, nivel):
        """Lista materiales por tema y nivel"""
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
    def listar_por_nivel(cls, nivel):
        """Lista todos los materiales de un nivel"""
        if nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        return cls.find({'nivel': nivel, 'activo': True}, sort=[('orden', 1)])

    @classmethod
    def actualizar(cls, material_id, datos):
        """Actualiza un material"""
        if isinstance(material_id, str):
            material_id = ObjectId(material_id)

        # Si se actualiza el nivel, validar
        if 'nivel' in datos and datos['nivel'] not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(cls.NIVELES)}")

        # Si se actualiza el tema_id, validar que existe y actualizar tema_nombre
        if 'tema_id' in datos:
            tema_id = datos['tema_id']
            if isinstance(tema_id, str):
                tema_id = ObjectId(tema_id)
            tema = Tema.find_one({'_id': tema_id})
            if not tema:
                raise ValueError("El tema especificado no existe")
            datos['tema_nombre'] = tema['nombre']

        return cls.update_one({'_id': material_id}, datos)

    @classmethod
    def agregar_recurso(cls, material_id, url_recurso, tipo='imagen', descripcion=''):
        """Agrega un recurso multimedia al material"""
        if isinstance(material_id, str):
            material_id = ObjectId(material_id)

        material = cls.find_one({'_id': material_id})
        if not material:
            raise ValueError("El material especificado no existe")

        recurso = {
            'url': url_recurso,
            'tipo': tipo,  # imagen, audio, video
            'descripcion': descripcion,
            'agregado_en': datetime.utcnow()
        }

        # Agregar recurso al array
        return cls.get_collection().update_one(
            {'_id': material_id},
            {
                '$push': {'recursos': recurso},
                '$set': {'actualizado_en': datetime.utcnow()}
            }
        )


class Vocabulario(MongoDBModel):
    """Modelo para palabras del vocabulario maya"""
    collection_name = 'vocabulario'

    @classmethod
    def crear(cls, tema_id, palabra_maya, palabra_espanol, pronunciacion='',
              imagen_url='', audio_url='', nivel='Básico'):
        """Crea una nueva palabra del vocabulario"""
        if nivel not in Material.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(Material.NIVELES)}")

        # Verificar que el tema existe
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        tema = Tema.find_one({'_id': tema_id})
        if not tema:
            raise ValueError("El tema especificado no existe")

        data = {
            'tema_id': tema_id,
            'tema_nombre': tema['nombre'],
            'palabra_maya': palabra_maya,
            'palabra_espanol': palabra_espanol,
            'pronunciacion': pronunciacion,
            'imagen_url': imagen_url,
            'audio_url': audio_url,
            'nivel': nivel,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_id(cls, vocabulario_id):
        """Obtiene una palabra por ID"""
        if isinstance(vocabulario_id, str):
            vocabulario_id = ObjectId(vocabulario_id)
        return cls.find_one({'_id': vocabulario_id})

    @classmethod
    def listar_por_tema(cls, tema_id):
        """Lista vocabulario por tema"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)
        return cls.find({'tema_id': tema_id, 'activo': True})

    @classmethod
    def listar_por_tema_y_nivel(cls, tema_id, nivel):
        """Lista vocabulario por tema y nivel"""
        if isinstance(tema_id, str):
            tema_id = ObjectId(tema_id)

        if nivel not in Material.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(Material.NIVELES)}")

        return cls.find({
            'tema_id': tema_id,
            'nivel': nivel,
            'activo': True
        })

    @classmethod
    def buscar_palabra(cls, palabra):
        """Busca una palabra en maya o español"""
        return cls.find({
            '$or': [
                {'palabra_maya': {'$regex': palabra, '$options': 'i'}},
                {'palabra_espanol': {'$regex': palabra, '$options': 'i'}}
            ],
            'activo': True
        })

    @classmethod
    def actualizar(cls, vocabulario_id, datos):
        """Actualiza una palabra del vocabulario"""
        if isinstance(vocabulario_id, str):
            vocabulario_id = ObjectId(vocabulario_id)

        # Si se actualiza el nivel, validar
        if 'nivel' in datos and datos['nivel'] not in Material.NIVELES:
            raise ValueError(f"Nivel debe ser uno de: {', '.join(Material.NIVELES)}")

        # Si se actualiza el tema_id, validar que existe
        if 'tema_id' in datos:
            tema_id = datos['tema_id']
            if isinstance(tema_id, str):
                tema_id = ObjectId(tema_id)
            tema = Tema.find_one({'_id': tema_id})
            if not tema:
                raise ValueError("El tema especificado no existe")
            datos['tema_nombre'] = tema['nombre']

        return cls.update_one({'_id': vocabulario_id}, datos)
