from django.core.management.base import BaseCommand
from usuarios.models import Grupo, Administrador, Alumno
from contenido.models import Tema, Material, Vocabulario
from evaluaciones.models import Actividad, IntentoPrueba, Calificacion


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos iniciales de ejemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando población de datos...'))

        # Limpiar colecciones existentes (opcional - comentar si no quieres borrar datos)
        self.stdout.write('Limpiando datos existentes...')
        self._limpiar_datos()

        # 1. Crear Grupos
        self.stdout.write('\n1. Creando grupos...')
        grupos = self._crear_grupos()

        # 2. Crear Administradores
        self.stdout.write('\n2. Creando administradores...')
        admins = self._crear_administradores()

        # 3. Crear Alumnos
        self.stdout.write('\n3. Creando alumnos...')
        alumnos = self._crear_alumnos(grupos)

        # 4. Crear Temas
        self.stdout.write('\n4. Creando temas...')
        temas = self._crear_temas()

        # 5. Crear Materiales
        self.stdout.write('\n5. Creando materiales...')
        materiales = self._crear_materiales(temas)

        # 6. Crear Vocabulario
        self.stdout.write('\n6. Creando vocabulario...')
        vocabulario = self._crear_vocabulario(temas)

        # 7. Crear Actividades
        self.stdout.write('\n7. Creando actividades...')
        actividades = self._crear_actividades(temas)

        self.stdout.write(self.style.SUCCESS('\n✓ Base de datos poblada exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'\nResumen:'))
        self.stdout.write(f'  - {len(grupos)} grupos')
        self.stdout.write(f'  - {len(admins)} administradores')
        self.stdout.write(f'  - {len(alumnos)} alumnos')
        self.stdout.write(f'  - {len(temas)} temas')
        self.stdout.write(f'  - {len(materiales)} materiales')
        self.stdout.write(f'  - {len(vocabulario)} palabras de vocabulario')
        self.stdout.write(f'  - {len(actividades)} actividades')

        # Mostrar credenciales
        self.stdout.write(self.style.WARNING('\n--- Credenciales de acceso ---'))
        self.stdout.write('Administrador:')
        self.stdout.write('  Email: admin@maya.edu')
        self.stdout.write('  Password: admin123')
        self.stdout.write('\nAlumno ejemplo:')
        self.stdout.write('  Email: juan.pech@alumno.com')
        self.stdout.write('  Password: alumno123')

    def _limpiar_datos(self):
        """Limpia todas las colecciones"""
        try:
            Grupo.get_collection().delete_many({})
            Alumno.get_collection().delete_many({})
            Administrador.get_collection().delete_many({})
            Tema.get_collection().delete_many({})
            Material.get_collection().delete_many({})
            Vocabulario.get_collection().delete_many({})
            Actividad.get_collection().delete_many({})
            IntentoPrueba.get_collection().delete_many({})
            Calificacion.get_collection().delete_many({})
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Advertencia al limpiar: {e}'))

    def _crear_grupos(self):
        """Crea los grupos A y B"""
        grupos = []
        try:
            grupo_a_id = Grupo.crear('A', 'Grupo A - Turno matutino')
            grupos.append({'id': grupo_a_id, 'nombre': 'A'})
            self.stdout.write(self.style.SUCCESS('  ✓ Grupo A creado'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Grupo A: {e}'))

        try:
            grupo_b_id = Grupo.crear('B', 'Grupo B - Turno vespertino')
            grupos.append({'id': grupo_b_id, 'nombre': 'B'})
            self.stdout.write(self.style.SUCCESS('  ✓ Grupo B creado'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Grupo B: {e}'))

        return grupos

    def _crear_administradores(self):
        """Crea 5 administradores"""
        admins = []
        administradores_data = [
            ('admin@maya.edu', 'admin123', 'Carlos', 'López'),
            ('profesor1@maya.edu', 'prof123', 'María', 'González'),
            ('profesor2@maya.edu', 'prof123', 'José', 'Martínez'),
            ('profesor3@maya.edu', 'prof123', 'Ana', 'Hernández'),
            ('profesor4@maya.edu', 'prof123', 'Luis', 'Ramírez'),
        ]

        for email, password, nombre, apellido in administradores_data:
            try:
                admin_id = Administrador.crear_admin(email, password, nombre, apellido)
                admins.append(admin_id)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Admin creado: {nombre} {apellido}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return admins

    def _crear_alumnos(self, grupos):
        """Crea 10 alumnos (5 por grupo)"""
        if not grupos:
            self.stdout.write(self.style.ERROR('  No hay grupos disponibles'))
            return []

        alumnos = []
        alumnos_data = [
            # Grupo A
            ('juan.pech@alumno.com', 'alumno123', 'Juan', 'Pech', 'A', 'Básico'),
            ('maria.chan@alumno.com', 'alumno123', 'María', 'Chan', 'A', 'Intermedio'),
            ('pedro.uc@alumno.com', 'alumno123', 'Pedro', 'Uc', 'A', 'Avanzado'),
            ('lucia.may@alumno.com', 'alumno123', 'Lucía', 'May', 'A', 'Básico'),
            ('carlos.ku@alumno.com', 'alumno123', 'Carlos', 'Ku', 'A', 'Intermedio'),
            # Grupo B
            ('ana.tun@alumno.com', 'alumno123', 'Ana', 'Tun', 'B', 'Básico'),
            ('diego.pool@alumno.com', 'alumno123', 'Diego', 'Pool', 'B', 'Intermedio'),
            ('sofia.canche@alumno.com', 'alumno123', 'Sofía', 'Canché', 'B', 'Avanzado'),
            ('miguel.balam@alumno.com', 'alumno123', 'Miguel', 'Balam', 'B', 'Básico'),
            ('elena.dzul@alumno.com', 'alumno123', 'Elena', 'Dzul', 'B', 'Intermedio'),
        ]

        for email, password, nombre, apellido, grupo_nombre, nivel in alumnos_data:
            try:
                # Buscar el grupo
                grupo = next((g for g in grupos if g['nombre'] == grupo_nombre), None)
                if grupo:
                    alumno_id = Alumno.crear_alumno(
                        email, password, nombre, apellido, grupo['id'], nivel
                    )
                    alumnos.append(alumno_id)
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Alumno creado: {nombre} {apellido} - Grupo {grupo_nombre} ({nivel})'
                    ))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return alumnos

    def _crear_temas(self):
        """Crea los 4 temas principales"""
        temas = []
        temas_data = [
            ('Números', 'Aprende los números en maya del 0 al 100', 1),
            ('Comidas', 'Vocabulario de alimentos y comidas típicas', 2),
            ('Objetos Cotidianos', 'Objetos de uso diario en maya', 3),
            ('Animales', 'Nombres de animales en lengua maya', 4),
        ]

        for nombre, descripcion, orden in temas_data:
            try:
                tema_id = Tema.crear(nombre, descripcion, orden)
                temas.append({'id': tema_id, 'nombre': nombre})
                self.stdout.write(self.style.SUCCESS(f'  ✓ Tema creado: {nombre}'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return temas

    def _crear_materiales(self, temas):
        """Crea materiales educativos para cada tema y nivel"""
        if not temas:
            return []

        materiales = []
        niveles = ['Básico', 'Intermedio', 'Avanzado']

        for tema in temas:
            for idx, nivel in enumerate(niveles):
                try:
                    material_id = Material.crear(
                        tema_id=tema['id'],
                        nivel=nivel,
                        titulo=f"Introducción a {tema['nombre']} - {nivel}",
                        contenido=f"Este material te enseñará sobre {tema['nombre'].lower()} en lengua maya. "
                                  f"Nivel {nivel}: contenido adaptado para estudiantes de nivel {nivel.lower()}.",
                        recursos=[
                            {
                                'url': f'/media/{tema["nombre"].lower()}_ejemplo.jpg',
                                'tipo': 'imagen',
                                'descripcion': f'Imagen de ejemplo de {tema["nombre"].lower()}'
                            }
                        ],
                        orden=idx
                    )
                    materiales.append(material_id)
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Material: {tema["nombre"]} - {nivel}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return materiales

    def _crear_vocabulario(self, temas):
        """Crea palabras de vocabulario para cada tema"""
        if not temas:
            return []

        vocabulario = []

        # Vocabulario por tema
        vocab_data = {
            'Números': [
                ('hun', 'uno', 'jun', 'Básico'),
                ('ka\'a', 'dos', 'ka-a', 'Básico'),
                ('óox', 'tres', 'óox', 'Básico'),
                ('kan', 'cuatro', 'kan', 'Intermedio'),
                ('ho\'o', 'cinco', 'jo-o', 'Intermedio'),
            ],
            'Comidas': [
                ('wa', 'tortilla', 'wa', 'Básico'),
                ('bu\'ul', 'frijol', 'bu-ul', 'Básico'),
                ('ha\'a', 'agua', 'ja-a', 'Básico'),
                ('sak ha\'', 'atole', 'sak ja', 'Intermedio'),
                ('mukbil pollo', 'tamal de pollo', 'muk-bil po-yo', 'Avanzado'),
            ],
            'Objetos Cotidianos': [
                ('k\'áax', 'bosque', 'k-aax', 'Básico'),
                ('otoch', 'casa', 'o-toch', 'Básico'),
                ('k\'áat', 'hamaca', 'k-aat', 'Básico'),
                ('ch\'uy', 'jícara', 'ch-uy', 'Intermedio'),
                ('p\'iis', 'medida', 'p-iis', 'Avanzado'),
            ],
            'Animales': [
                ('peek\'', 'perro', 'pe-ek', 'Básico'),
                ('mis', 'gato', 'mis', 'Básico'),
                ('ch\'iich\'', 'pájaro', 'ch-iich', 'Básico'),
                ('kéej', 'venado', 'ke-ej', 'Intermedio'),
                ('báalam', 'jaguar', 'ba-lam', 'Avanzado'),
            ],
        }

        for tema in temas:
            if tema['nombre'] in vocab_data:
                for palabra_maya, palabra_espanol, pronunciacion, nivel in vocab_data[tema['nombre']]:
                    try:
                        vocab_id = Vocabulario.crear(
                            tema_id=tema['id'],
                            palabra_maya=palabra_maya,
                            palabra_espanol=palabra_espanol,
                            pronunciacion=pronunciacion,
                            nivel=nivel
                        )
                        vocabulario.append(vocab_id)
                        self.stdout.write(self.style.SUCCESS(
                            f'  ✓ Vocabulario: {palabra_maya} = {palabra_espanol}'
                        ))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return vocabulario

    def _crear_actividades(self, temas):
        """Crea actividades para cada tema"""
        if not temas:
            return []

        actividades = []
        niveles = ['Básico', 'Intermedio', 'Avanzado']

        for tema in temas:
            for nivel in niveles:
                try:
                    # Crear actividad
                    actividad_id = Actividad.crear(
                        tema_id=tema['id'],
                        nivel=nivel,
                        titulo=f"Quiz de {tema['nombre']} - {nivel}",
                        descripcion=f"Evalúa tus conocimientos sobre {tema['nombre'].lower()} en nivel {nivel.lower()}",
                        tipo='opcion_multiple',
                        duracion_minutos=10,
                        orden=niveles.index(nivel)
                    )

                    # Agregar 3 preguntas de ejemplo
                    preguntas = self._obtener_preguntas_ejemplo(tema['nombre'], nivel)
                    for pregunta in preguntas:
                        Actividad.agregar_pregunta(
                            actividad_id,
                            pregunta['texto'],
                            pregunta['respuesta_correcta'],
                            pregunta['opciones'],
                            pregunta['puntos']
                        )

                    actividades.append(actividad_id)
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Actividad: {tema["nombre"]} - {nivel} (con {len(preguntas)} preguntas)'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  Error: {e}'))

        return actividades

    def _obtener_preguntas_ejemplo(self, tema_nombre, nivel):
        """Retorna preguntas de ejemplo según el tema"""
        preguntas_base = {
            'Números': [
                {
                    'texto': '¿Cómo se dice "uno" en maya?',
                    'opciones': ['hun', 'ka\'a', 'óox', 'kan'],
                    'respuesta_correcta': 'hun',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "dos" en maya?',
                    'opciones': ['hun', 'ka\'a', 'óox', 'kan'],
                    'respuesta_correcta': 'ka\'a',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "tres" en maya?',
                    'opciones': ['hun', 'ka\'a', 'óox', 'kan'],
                    'respuesta_correcta': 'óox',
                    'puntos': 10
                },
            ],
            'Comidas': [
                {
                    'texto': '¿Cómo se dice "tortilla" en maya?',
                    'opciones': ['wa', 'bu\'ul', 'ha\'a', 'sak ha\''],
                    'respuesta_correcta': 'wa',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "frijol" en maya?',
                    'opciones': ['wa', 'bu\'ul', 'ha\'a', 'sak ha\''],
                    'respuesta_correcta': 'bu\'ul',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "agua" en maya?',
                    'opciones': ['wa', 'bu\'ul', 'ha\'a', 'sak ha\''],
                    'respuesta_correcta': 'ha\'a',
                    'puntos': 10
                },
            ],
            'Objetos Cotidianos': [
                {
                    'texto': '¿Cómo se dice "casa" en maya?',
                    'opciones': ['otoch', 'k\'áat', 'ch\'uy', 'p\'iis'],
                    'respuesta_correcta': 'otoch',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "hamaca" en maya?',
                    'opciones': ['otoch', 'k\'áat', 'ch\'uy', 'p\'iis'],
                    'respuesta_correcta': 'k\'áat',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "jícara" en maya?',
                    'opciones': ['otoch', 'k\'áat', 'ch\'uy', 'p\'iis'],
                    'respuesta_correcta': 'ch\'uy',
                    'puntos': 10
                },
            ],
            'Animales': [
                {
                    'texto': '¿Cómo se dice "perro" en maya?',
                    'opciones': ['peek\'', 'mis', 'ch\'iich\'', 'kéej'],
                    'respuesta_correcta': 'peek\'',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "gato" en maya?',
                    'opciones': ['peek\'', 'mis', 'ch\'iich\'', 'kéej'],
                    'respuesta_correcta': 'mis',
                    'puntos': 10
                },
                {
                    'texto': '¿Cómo se dice "pájaro" en maya?',
                    'opciones': ['peek\'', 'mis', 'ch\'iich\'', 'kéej'],
                    'respuesta_correcta': 'ch\'iich\'',
                    'puntos': 10
                },
            ],
        }

        return preguntas_base.get(tema_nombre, [])
