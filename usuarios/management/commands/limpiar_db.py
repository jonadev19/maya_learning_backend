from django.core.management.base import BaseCommand
from usuarios.models import Grupo, Administrador, Alumno, Usuario
from django.conf import settings


class Command(BaseCommand):
    help = 'Limpia todas las colecciones de la base de datos MongoDB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirma que deseas eliminar todos los datos',
        )

    def handle(self, *args, **options):
        if not options['confirmar']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ADVERTENCIA: Este comando eliminará TODOS los datos de la base de datos.\n'
                    'Para confirmar, ejecuta: python manage.py limpiar_db --confirmar'
                )
            )
            return

        self.stdout.write(self.style.WARNING('\n🗑️  Limpiando base de datos MongoDB...'))

        try:
            # Obtener referencia a la base de datos
            db = settings.MONGO_DB

            if db is None:
                self.stdout.write(self.style.ERROR('✗ MongoDB no está conectado'))
                return

            # Listar todas las colecciones
            colecciones = db.list_collection_names()

            if not colecciones:
                self.stdout.write(self.style.SUCCESS('✓ La base de datos ya está vacía'))
                return

            self.stdout.write(f'\nColecciones encontradas: {len(colecciones)}')

            # Limpiar cada colección
            eliminadas = 0
            for coleccion_nombre in colecciones:
                try:
                    resultado = db[coleccion_nombre].delete_many({})
                    if resultado.deleted_count > 0:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✓ {coleccion_nombre}: {resultado.deleted_count} documentos eliminados'
                            )
                        )
                        eliminadas += 1
                    else:
                        self.stdout.write(f'  • {coleccion_nombre}: vacía')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ✗ Error en {coleccion_nombre}: {e}')
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Base de datos limpiada exitosamente!'
                    f'\n  Colecciones procesadas: {len(colecciones)}'
                    f'\n  Colecciones con datos eliminados: {eliminadas}'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error al limpiar la base de datos: {e}'))