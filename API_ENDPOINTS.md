# Documentación API - Maya Backend

API REST para la aplicación de enseñanza del lenguaje maya.

**Base URL:** `http://localhost:8000/api/`

---

## 📚 Índice

1. [Autenticación](#autenticación)
2. [Usuarios](#usuarios)
3. [Contenido](#contenido)
4. [Evaluaciones](#evaluaciones)
5. [Reportes](#reportes)

---

## Autenticación

La API utiliza **JWT (JSON Web Tokens)** para la autenticación. La mayoría de los endpoints requieren autenticación.

### Login

#### Iniciar sesión
```
POST /api/auth/login/
```
**Cuerpo:**
```json
{
  "email": "admin@maya.edu",
  "password": "admin123"
}
```
**Respuesta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "admin@maya.edu",
    "nombre": "Carlos",
    "apellido": "López",
    "rol": "administrador"
  }
}
```

**Nota:** Guarda el `access` token para usarlo en las peticiones subsecuentes.

---

### Refresh Token

#### Refrescar el token de acceso
```
POST /api/auth/refresh/
```
**Cuerpo:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Respuesta (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Logout

#### Cerrar sesión
```
POST /api/auth/logout/
```
**Autenticación:** Requerida

**Header:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Cuerpo:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Respuesta (200 OK):**
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

---

### Usuario Actual

#### Obtener información del usuario autenticado
```
GET /api/auth/me/
```
**Autenticación:** Requerida

**Header:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "admin@maya.edu",
  "nombre": "Carlos",
  "apellido": "López",
  "rol": "administrador",
  "activo": true
}
```

---

### Uso de Autenticación en Endpoints

Para acceder a endpoints protegidos, incluye el token de acceso en el header `Authorization`:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Ejemplo con curl:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://localhost:8000/api/grupos/
```

---

### Permisos

Los endpoints tienen diferentes niveles de permisos:

- **Públicos:** Login (no requieren autenticación)
- **Autenticados:** Requieren token válido
- **Solo Administradores:** Solo usuarios con rol `administrador`
- **Lectura para todos, Escritura solo Administradores:** Todos los autenticados pueden leer, solo administradores pueden crear/editar

#### Permisos por Endpoint:

| Endpoint | GET | POST | PUT/PATCH | DELETE |
|----------|-----|------|-----------|--------|
| `/auth/login/` | - | Público | - | - |
| `/auth/refresh/` | - | Público | - | - |
| `/auth/logout/` | - | Autenticado | - | - |
| `/auth/me/` | Autenticado | - | - | - |
| `/grupos/` | Autenticado | Admin | - | - |
| `/administradores/` | Admin | Admin | - | - |
| `/alumnos/` | Autenticado | Admin | - | - |
| `/usuarios/` | Autenticado | - | - | - |

---

## Usuarios

### Grupos

#### Listar todos los grupos
```
GET /api/grupos/
```
**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "nombre": "A",
    "descripcion": "Grupo A - Turno matutino",
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Crear un nuevo grupo
```
POST /api/grupos/
```
**Cuerpo de la petición:**
```json
{
  "nombre": "A",
  "descripcion": "Grupo A - Turno matutino"
}
```
**Respuesta (201 CREATED):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "nombre": "A",
  "descripcion": "Grupo A - Turno matutino",
  "activo": true,
  "creado_en": "2024-01-15T10:30:00Z",
  "actualizado_en": "2024-01-15T10:30:00Z"
}
```

#### Obtener detalle de un grupo
```
GET /api/grupos/<id>/
```

---

### Administradores

#### Listar todos los administradores
```
GET /api/administradores/
```
**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "email": "admin@maya.edu",
    "nombre": "Carlos",
    "apellido": "López",
    "rol": "administrador",
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de un administrador
```
GET /api/administradores/<id>/
```

---

### Alumnos

#### Listar todos los alumnos
```
GET /api/alumnos/
```

**Parámetros de consulta opcionales:**
- `grupo` - Filtrar por grupo (A o B)
- `nivel` - Filtrar por nivel (Básico, Intermedio, Avanzado)

**Ejemplos:**
```
GET /api/alumnos/?grupo=A
GET /api/alumnos/?nivel=Básico
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "email": "juan.pech@alumno.com",
    "nombre": "Juan",
    "apellido": "Pech",
    "rol": "alumno",
    "grupo_id": "507f1f77bcf86cd799439012",
    "grupo_nombre": "A",
    "nivel": "Básico",
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de un alumno
```
GET /api/alumnos/<id>/
```

---

### Usuarios (todos)

#### Listar todos los usuarios
```
GET /api/usuarios/
```

**Parámetros de consulta opcionales:**
- `rol` - Filtrar por rol (administrador o alumno)

**Ejemplo:**
```
GET /api/usuarios/?rol=alumno
```

#### Obtener detalle de un usuario
```
GET /api/usuarios/<id>/
```

---

## Contenido

### Temas

#### Listar todos los temas
```
GET /api/temas/
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "nombre": "Números",
    "descripcion": "Aprende los números en maya del 0 al 100",
    "orden": 1,
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

**Temas disponibles:**
- Números
- Comidas
- Objetos Cotidianos
- Animales

#### Obtener detalle de un tema
```
GET /api/temas/<id>/
```

---

### Materiales

#### Listar todos los materiales educativos
```
GET /api/materiales/
```

**Parámetros de consulta opcionales:**
- `tema_id` - Filtrar por tema
- `nivel` - Filtrar por nivel (Básico, Intermedio, Avanzado)

**Ejemplos:**
```
GET /api/materiales/?tema_id=507f1f77bcf86cd799439011
GET /api/materiales/?nivel=Básico
GET /api/materiales/?tema_id=507f1f77bcf86cd799439011&nivel=Básico
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "tema_id": "507f1f77bcf86cd799439012",
    "tema_nombre": "Números",
    "nivel": "Básico",
    "titulo": "Introducción a Números - Básico",
    "contenido": "Este material te enseñará sobre números en lengua maya...",
    "recursos": [
      {
        "url": "/media/numeros_ejemplo.jpg",
        "tipo": "imagen",
        "descripcion": "Imagen de ejemplo de números",
        "agregado_en": "2024-01-15T10:30:00Z"
      }
    ],
    "orden": 0,
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de un material
```
GET /api/materiales/<id>/
```

---

### Vocabulario

#### Listar palabras del vocabulario
```
GET /api/vocabulario/
```

**Parámetros de consulta opcionales:**
- `tema_id` - Filtrar por tema
- `nivel` - Filtrar por nivel (Básico, Intermedio, Avanzado)
- `buscar` - Buscar palabra en maya o español

**Ejemplos:**
```
GET /api/vocabulario/?tema_id=507f1f77bcf86cd799439011
GET /api/vocabulario/?nivel=Básico
GET /api/vocabulario/?buscar=perro
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "tema_id": "507f1f77bcf86cd799439012",
    "tema_nombre": "Animales",
    "palabra_maya": "peek'",
    "palabra_espanol": "perro",
    "pronunciacion": "pe-ek",
    "imagen_url": "",
    "audio_url": "",
    "nivel": "Básico",
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de una palabra
```
GET /api/vocabulario/<id>/
```

---

## Evaluaciones

### Actividades

#### Listar todas las actividades
```
GET /api/actividades/
```

**Parámetros de consulta opcionales:**
- `tema_id` - Filtrar por tema
- `nivel` - Filtrar por nivel (Básico, Intermedio, Avanzado)

**Ejemplos:**
```
GET /api/actividades/?tema_id=507f1f77bcf86cd799439011
GET /api/actividades/?nivel=Básico
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "tema_id": "507f1f77bcf86cd799439012",
    "tema_nombre": "Números",
    "nivel": "Básico",
    "titulo": "Quiz de Números - Básico",
    "descripcion": "Evalúa tus conocimientos sobre números en nivel básico",
    "tipo": "opcion_multiple",
    "duracion_minutos": 10,
    "orden": 0,
    "preguntas": [
      {
        "id": "507f1f77bcf86cd799439013",
        "texto": "¿Cómo se dice 'uno' en maya?",
        "tipo": "opcion_multiple",
        "opciones": ["hun", "ka'a", "óox", "kan"],
        "respuesta_correcta": "hun",
        "puntos": 10,
        "orden": 0
      }
    ],
    "puntaje_total": 30,
    "activo": true,
    "creado_en": "2024-01-15T10:30:00Z",
    "actualizado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de una actividad
```
GET /api/actividades/<id>/
```

---

### Intentos de Prueba

#### Listar intentos de prueba
```
GET /api/intentos/
```

**Parámetros de consulta opcionales:**
- `alumno_id` - Filtrar por alumno
- `actividad_id` - Filtrar por actividad

**Ejemplos:**
```
GET /api/intentos/?alumno_id=507f1f77bcf86cd799439011
GET /api/intentos/?actividad_id=507f1f77bcf86cd799439012
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "alumno_id": "507f1f77bcf86cd799439012",
    "alumno_nombre": "Juan Pech",
    "alumno_email": "juan.pech@alumno.com",
    "grupo_nombre": "A",
    "actividad_id": "507f1f77bcf86cd799439013",
    "actividad_titulo": "Quiz de Números - Básico",
    "tema_nombre": "Números",
    "nivel": "Básico",
    "fecha_inicio": "2024-01-15T10:30:00Z",
    "fecha_finalizacion": "2024-01-15T10:45:00Z",
    "estado": "completada",
    "respuestas": [
      {
        "pregunta_id": "507f1f77bcf86cd799439014",
        "respuesta_alumno": "hun",
        "es_correcta": true,
        "puntos_obtenidos": 10,
        "fecha_respuesta": "2024-01-15T10:32:00Z"
      }
    ],
    "puntaje_obtenido": 25,
    "puntaje_total": 30,
    "creado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de un intento
```
GET /api/intentos/<id>/
```

---

### Calificaciones

#### Listar calificaciones
```
GET /api/calificaciones/
```

**Parámetros de consulta opcionales:**
- `alumno_id` - Filtrar por alumno
- `grupo` - Filtrar por grupo (A o B)
- `tema` - Filtrar por tema
- `actividad_id` - Filtrar por actividad

**Ejemplos:**
```
GET /api/calificaciones/?alumno_id=507f1f77bcf86cd799439011
GET /api/calificaciones/?grupo=A
GET /api/calificaciones/?tema=Números
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "alumno_id": "507f1f77bcf86cd799439012",
    "alumno_nombre": "Juan Pech",
    "alumno_email": "juan.pech@alumno.com",
    "grupo_nombre": "A",
    "actividad_id": "507f1f77bcf86cd799439013",
    "actividad_titulo": "Quiz de Números - Básico",
    "tema_nombre": "Números",
    "nivel": "Básico",
    "intento_id": "507f1f77bcf86cd799439014",
    "puntaje_obtenido": 25,
    "puntaje_total": 30,
    "porcentaje": 83.33,
    "aprobado": true,
    "fecha_evaluacion": "2024-01-15T10:45:00Z",
    "duracion_minutos": 15.0,
    "creado_en": "2024-01-15T10:45:00Z"
  }
]
```

#### Obtener detalle de una calificación
```
GET /api/calificaciones/<id>/
```

---

### Promedios y Estadísticas

#### Obtener promedio de un alumno
```
GET /api/calificaciones/promedio/<alumno_id>/
```

**Parámetros de consulta opcionales:**
- `tema` - Filtrar por tema específico

**Ejemplo:**
```
GET /api/calificaciones/promedio/507f1f77bcf86cd799439011/
GET /api/calificaciones/promedio/507f1f77bcf86cd799439011/?tema=Números
```

**Respuesta:**
```json
{
  "alumno_id": "507f1f77bcf86cd799439011",
  "tema_nombre": null,
  "promedio": 85.50
}
```

---

#### Obtener promedio de un grupo
```
GET /api/calificaciones/promedio-grupo/<grupo_nombre>/
```

**Parámetros de consulta opcionales:**
- `tema` - Filtrar por tema específico

**Ejemplo:**
```
GET /api/calificaciones/promedio-grupo/A/
GET /api/calificaciones/promedio-grupo/A/?tema=Números
```

**Respuesta:**
```json
{
  "grupo_nombre": "A",
  "tema_nombre": null,
  "promedio": 78.25
}
```

---

#### Obtener estadísticas de un tema
```
GET /api/calificaciones/estadisticas/<tema_nombre>/
```

**Parámetros de consulta opcionales:**
- `grupo` - Filtrar por grupo específico

**Ejemplo:**
```
GET /api/calificaciones/estadisticas/Números/
GET /api/calificaciones/estadisticas/Números/?grupo=A
```

**Respuesta:**
```json
{
  "total_evaluaciones": 20,
  "promedio": 82.5,
  "aprobados": 18,
  "reprobados": 2,
  "porcentaje_aprobacion": 90.0
}
```

---

## Reportes

### Reportes Generados

#### Listar reportes generados
```
GET /api/reportes/
```

**Parámetros de consulta opcionales:**
- `tipo` - Filtrar por tipo (individual, grupo, tema, general)
- `generado_por` - Filtrar por ID del administrador que generó el reporte
- `alumno_id` - Filtrar reportes de un alumno específico
- `grupo` - Filtrar reportes de un grupo
- `limite` - Limitar cantidad de resultados (default: 10)

**Ejemplos:**
```
GET /api/reportes/?tipo=individual
GET /api/reportes/?grupo=A
GET /api/reportes/?limite=20
```

**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "tipo": "individual",
    "generado_por_id": "507f1f77bcf86cd799439012",
    "titulo": "Reporte Individual - Juan Pech",
    "descripcion": "Calificaciones del alumno Juan Pech",
    "alumno_id": "507f1f77bcf86cd799439013",
    "grupo_nombre": null,
    "tema_nombre": null,
    "archivo_url": "/media/reportes/reporte_123.pdf",
    "metadatos": {
      "fecha_inicio": "2024-01-01",
      "fecha_fin": "2024-01-31"
    },
    "fecha_generacion": "2024-01-15T10:30:00Z",
    "creado_en": "2024-01-15T10:30:00Z"
  }
]
```

#### Obtener detalle de un reporte
```
GET /api/reportes/<id>/
```

---

## Endpoints POST Disponibles

### Usuarios

#### Crear Administrador
```
POST /api/administradores/
```
**Cuerpo:**
```json
{
  "email": "admin@maya.edu",
  "password": "admin123",
  "nombre": "Carlos",
  "apellido": "López"
}
```

#### Crear Alumno
```
POST /api/alumnos/
```
**Cuerpo:**
```json
{
  "email": "juan.pech@alumno.com",
  "password": "alumno123",
  "nombre": "Juan",
  "apellido": "Pech",
  "grupo_id": "507f1f77bcf86cd799439012",
  "nivel": "Básico"
}
```

### Contenido

#### Crear Tema
```
POST /api/temas/
```
**Cuerpo:**
```json
{
  "nombre": "Números",
  "descripcion": "Aprende los números en maya",
  "orden": 1
}
```

#### Crear Material
```
POST /api/materiales/
```
**Cuerpo:**
```json
{
  "tema_id": "507f1f77bcf86cd799439011",
  "nivel": "Básico",
  "titulo": "Introducción a Números",
  "contenido": "Este material te enseñará...",
  "recursos": [],
  "orden": 0
}
```

#### Crear Vocabulario
```
POST /api/vocabulario/
```
**Cuerpo:**
```json
{
  "tema_id": "507f1f77bcf86cd799439011",
  "palabra_maya": "peek'",
  "palabra_espanol": "perro",
  "pronunciacion": "pe-ek",
  "imagen_url": "",
  "audio_url": "",
  "nivel": "Básico"
}
```

### Evaluaciones

#### Crear Actividad
```
POST /api/actividades/
```
**Cuerpo:**
```json
{
  "tema_id": "507f1f77bcf86cd799439011",
  "nivel": "Básico",
  "titulo": "Quiz de Números - Básico",
  "descripcion": "Evalúa tus conocimientos",
  "tipo": "opcion_multiple",
  "duracion_minutos": 10,
  "orden": 0
}
```

#### Agregar Pregunta a Actividad
```
POST /api/actividades/<id>/preguntas/
```
**Cuerpo:**
```json
{
  "texto": "¿Cómo se dice 'uno' en maya?",
  "tipo": "opcion_multiple",
  "opciones": ["hun", "ka'a", "óox", "kan"],
  "respuesta_correcta": "hun",
  "puntos": 10
}
```

#### Crear Intento de Prueba
```
POST /api/intentos/crear/
```
**Cuerpo:**
```json
{
  "alumno_id": "507f1f77bcf86cd799439011",
  "actividad_id": "507f1f77bcf86cd799439012"
}
```

#### Registrar Respuesta
```
POST /api/intentos/<id>/respuestas/
```
**Cuerpo:**
```json
{
  "pregunta_id": "507f1f77bcf86cd799439013",
  "respuesta_alumno": "hun"
}
```

#### Finalizar Intento (Genera calificación automáticamente)
```
POST /api/intentos/<id>/finalizar/
```
**Sin cuerpo** - Retorna la calificación generada.

#### Crear Calificación desde Intento
```
POST /api/calificaciones/crear/
```
**Cuerpo:**
```json
{
  "intento_id": "507f1f77bcf86cd799439011"
}
```

### Reportes

#### Crear Reporte
```
POST /api/reportes/
```
**Cuerpo:**
```json
{
  "tipo": "individual",
  "generado_por_id": "507f1f77bcf86cd799439011",
  "titulo": "Reporte Individual - Juan Pech",
  "descripcion": "Calificaciones del alumno",
  "alumno_id": "507f1f77bcf86cd799439012",
  "grupo_nombre": null,
  "tema_nombre": null,
  "archivo_url": "/media/reportes/reporte_123.pdf",
  "metadatos": {
    "fecha_inicio": "2024-01-01",
    "fecha_fin": "2024-01-31"
  }
}
```

---

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 CREATED` - Recurso creado exitosamente
- `400 Bad Request` - Parámetros inválidos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## Notas

1. Todos los IDs son ObjectId de MongoDB en formato string
2. Las fechas están en formato ISO 8601 (UTC)
3. Los filtros son case-sensitive
4. Para probar los endpoints, ejecuta: `python manage.py runserver`
5. Base URL local: `http://localhost:8000/api/`

---

## Credenciales de Prueba

**Administrador:**
- Email: `admin@maya.edu`
- Password: `admin123`

**Alumno:**
- Email: `juan.pech@alumno.com`
- Password: `alumno123`

---

**Nota:** Para poblar la base de datos con datos de ejemplo, ejecuta:
```bash
python manage.py poblar_datos
```
