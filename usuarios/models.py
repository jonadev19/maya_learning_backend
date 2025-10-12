from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
from datetime import datetime


class MongoDBModel:
    """Clase base para modelos de MongoDB"""
    collection_name = None

    @classmethod
    def get_collection(cls):
        """Obtiene la colección de MongoDB"""
        if settings.MONGO_DB is None:
            raise Exception("MongoDB no está conectado")
        return settings.MONGO_DB[cls.collection_name]

    @classmethod
    def find_one(cls, query):
        """Busca un documento"""
        return cls.get_collection().find_one(query)

    @classmethod
    def find(cls, query=None, **kwargs):
        """Busca múltiples documentos"""
        if query is None:
            query = {}
        return list(cls.get_collection().find(query, **kwargs))

    @classmethod
    def insert_one(cls, data):
        """Inserta un documento"""
        data['creado_en'] = datetime.utcnow()
        data['actualizado_en'] = datetime.utcnow()
        result = cls.get_collection().insert_one(data)
        return result.inserted_id

    @classmethod
    def update_one(cls, query, update_data):
        """Actualiza un documento"""
        update_data['actualizado_en'] = datetime.utcnow()
        return cls.get_collection().update_one(query, {'$set': update_data})

    @classmethod
    def delete_one(cls, query):
        """Elimina un documento"""
        return cls.get_collection().delete_one(query)

    @classmethod
    def count(cls, query=None):
        """Cuenta documentos"""
        if query is None:
            query = {}
        return cls.get_collection().count_documents(query)


class Grupo(MongoDBModel):
    """Modelo para Grupos (A, B)"""
    collection_name = 'grupos'

    # Opciones válidas para grupos
    GRUPOS_VALIDOS = ['A', 'B']

    @classmethod
    def crear(cls, nombre, descripcion=''):
        """Crea un nuevo grupo"""
        if nombre not in cls.GRUPOS_VALIDOS:
            raise ValueError(f"Grupo debe ser {' o '.join(cls.GRUPOS_VALIDOS)}")

        # Verificar si ya existe
        existente = cls.find_one({'nombre': nombre})
        if existente:
            raise ValueError(f"El grupo {nombre} ya existe")

        data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def obtener_por_nombre(cls, nombre):
        """Obtiene un grupo por nombre"""
        return cls.find_one({'nombre': nombre})

    @classmethod
    def listar_activos(cls):
        """Lista todos los grupos activos"""
        return cls.find({'activo': True})


class Usuario(MongoDBModel):
    """Modelo base para Usuarios"""
    collection_name = 'usuarios'

    ROLES = {
        'ADMIN': 'administrador',
        'ALUMNO': 'alumno'
    }

    @classmethod
    def crear(cls, email, password, nombre, apellido, rol):
        """Crea un nuevo usuario"""
        # Verificar si el email ya existe
        existente = cls.find_one({'email': email})
        if existente:
            raise ValueError("El email ya está registrado")

        if rol not in cls.ROLES.values():
            raise ValueError(f"Rol debe ser {' o '.join(cls.ROLES.values())}")

        data = {
            'email': email,
            'password': make_password(password),
            'nombre': nombre,
            'apellido': apellido,
            'rol': rol,
            'activo': True
        }
        return cls.insert_one(data)

    @classmethod
    def autenticar(cls, email, password):
        """Autentica un usuario"""
        usuario = cls.find_one({'email': email, 'activo': True})
        if usuario and check_password(password, usuario['password']):
            # No retornar la contraseña
            del usuario['password']
            return usuario
        return None

    @classmethod
    def obtener_por_id(cls, usuario_id):
        """Obtiene un usuario por ID"""
        if isinstance(usuario_id, str):
            usuario_id = ObjectId(usuario_id)
        usuario = cls.find_one({'_id': usuario_id})
        if usuario and 'password' in usuario:
            del usuario['password']
        return usuario

    @classmethod
    def obtener_por_email(cls, email):
        """Obtiene un usuario por email"""
        usuario = cls.find_one({'email': email})
        if usuario and 'password' in usuario:
            del usuario['password']
        return usuario

    @classmethod
    def listar_por_rol(cls, rol):
        """Lista usuarios por rol"""
        usuarios = cls.find({'rol': rol, 'activo': True})
        # Eliminar passwords de la lista
        for usuario in usuarios:
            if 'password' in usuario:
                del usuario['password']
        return usuarios


class Administrador(Usuario):
    """Modelo para Administradores (Profesores)"""

    @classmethod
    def crear_admin(cls, email, password, nombre, apellido):
        """Crea un administrador"""
        return cls.crear(email, password, nombre, apellido, cls.ROLES['ADMIN'])

    @classmethod
    def listar_todos(cls):
        """Lista todos los administradores"""
        return cls.listar_por_rol(cls.ROLES['ADMIN'])


class Alumno(Usuario):
    """Modelo para Alumnos"""

    # Niveles válidos
    NIVELES = ['Básico', 'Intermedio', 'Avanzado']

    @classmethod
    def crear_alumno(cls, email, password, nombre, apellido, grupo_id, nivel='Básico'):
        """Crea un alumno"""
        if nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser {', '.join(cls.NIVELES)}")

        # Verificar que el grupo existe
        if isinstance(grupo_id, str):
            grupo_id = ObjectId(grupo_id)

        grupo = Grupo.find_one({'_id': grupo_id})
        if not grupo:
            raise ValueError("El grupo especificado no existe")

        # Crear usuario base
        usuario_id = cls.crear(email, password, nombre, apellido, cls.ROLES['ALUMNO'])

        # Agregar información específica del alumno
        cls.update_one(
            {'_id': usuario_id},
            {
                'grupo_id': grupo_id,
                'grupo_nombre': grupo['nombre'],
                'nivel': nivel
            }
        )

        return usuario_id

    @classmethod
    def listar_todos(cls):
        """Lista todos los alumnos"""
        return cls.listar_por_rol(cls.ROLES['ALUMNO'])

    @classmethod
    def listar_por_grupo(cls, grupo_nombre):
        """Lista alumnos por grupo"""
        alumnos = cls.find({
            'rol': cls.ROLES['ALUMNO'],
            'grupo_nombre': grupo_nombre,
            'activo': True
        })
        for alumno in alumnos:
            if 'password' in alumno:
                del alumno['password']
        return alumnos

    @classmethod
    def listar_por_nivel(cls, nivel):
        """Lista alumnos por nivel"""
        alumnos = cls.find({
            'rol': cls.ROLES['ALUMNO'],
            'nivel': nivel,
            'activo': True
        })
        for alumno in alumnos:
            if 'password' in alumno:
                del alumno['password']
        return alumnos

    @classmethod
    def actualizar_nivel(cls, alumno_id, nuevo_nivel):
        """Actualiza el nivel de un alumno"""
        if nuevo_nivel not in cls.NIVELES:
            raise ValueError(f"Nivel debe ser {', '.join(cls.NIVELES)}")

        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)

        return cls.update_one(
            {'_id': alumno_id},
            {'nivel': nuevo_nivel}
        )

    @classmethod
    def cambiar_grupo(cls, alumno_id, nuevo_grupo_id):
        """Cambia el grupo de un alumno"""
        if isinstance(alumno_id, str):
            alumno_id = ObjectId(alumno_id)
        if isinstance(nuevo_grupo_id, str):
            nuevo_grupo_id = ObjectId(nuevo_grupo_id)

        grupo = Grupo.find_one({'_id': nuevo_grupo_id})
        if not grupo:
            raise ValueError("El grupo especificado no existe")

        return cls.update_one(
            {'_id': alumno_id},
            {
                'grupo_id': nuevo_grupo_id,
                'grupo_nombre': grupo['nombre']
            }
        )
