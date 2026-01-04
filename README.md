# 🌟 Maya Learning - Backend API

> Sistema backend para una aplicación móvil de enseñanza del lenguaje maya con gestión de usuarios, contenido educativo, evaluaciones y generación de reportes.

![Django](https://img.shields.io/badge/Django-5.2.7-green?style=flat&logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16.1-red?style=flat)
![MongoDB](https://img.shields.io/badge/MongoDB-3.11.4-green?style=flat&logo=mongodb)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)

---

## 📖 Descripción del Proyecto

**Maya Learning Backend** es una API REST desarrollada con Django y Django REST Framework que sirve como backend para una aplicación móvil educativa dedicada a la enseñanza del lenguaje maya. El sistema permite gestionar usuarios (administradores y alumnos), contenido educativo organizado por temas y niveles, actividades de evaluación, y generación de reportes en PDF.

### Contexto Educativo

El proyecto aborda la necesidad de preservar y enseñar el lenguaje maya mediante una plataforma digital moderna. Los contenidos están organizados en cuatro temas principales:
- 🔢 **Números** - Números del 0 al 100 en maya
- 🍽️ **Comidas** - Vocabulario de alimentos tradicionales
- 🏠 **Objetos Cotidianos** - Elementos del día a día
- 🦎 **Animales** - Fauna local y regional

---

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- Autenticación JWT (JSON Web Tokens) con access y refresh tokens
- Sistema de permisos basado en roles (Administrador/Alumno)
- Gestión segura de contraseñas con hashing
- Blacklist de tokens para logout seguro

### 👥 Gestión de Usuarios
- **Administradores**: Profesores con permisos completos
  - Crear, actualizar y desactivar usuarios
  - Gestionar contenido educativo
  - Generar reportes individuales y grupales
  - Ver calificaciones y estadísticas
  
- **Alumnos**: Estudiantes con acceso controlado
  - Acceder a materiales educativos
  - Realizar actividades y evaluaciones
  - Ver su progreso personal
  - Organizados por grupos (A, B) y niveles (Básico, Intermedio, Avanzado)

### 📚 Contenido Educativo
- **Temas**: Estructura organizativa de contenidos
- **Materiales**: Recursos educativos con soporte multimedia
- **Vocabulario**: Base de datos de palabras en maya con traducciones, pronunciación y recursos audiovisuales

### 📝 Sistema de Evaluaciones
- **Actividades**: Cuestionarios y ejercicios configurables
- **Preguntas**: Soporte para múltiples tipos (opción múltiple, verdadero/falso)
- **Intentos**: Registro detallado de cada intento de evaluación
- **Calificaciones**: Sistema automático de calificación con cálculo de promedios

### 📊 Reportes y Estadísticas
- Reportes individuales por alumno
- Reportes grupales
- Estadísticas por tema
- Generación de archivos PDF
- Cálculo de promedios y porcentajes de aprobación

---

## 🛠️ Tecnologías Utilizadas

### Backend Framework
- **Django 5.2.7** - Framework web de alto nivel
- **Django REST Framework 3.16.1** - Toolkit para construcción de APIs REST

### Base de Datos
- **MongoDB 3.11.4** - Base de datos NoSQL orientada a documentos
- **PyMongo** - Driver oficial de Python para MongoDB

### Autenticación y Seguridad
- **djangorestframework-simplejwt 5.5.1** - Autenticación JWT
- **PyJWT 2.10.1** - Librería de tokens JWT
- **Django password hashing** - Sistema seguro de hashing de contraseñas

### Herramientas Adicionales
- **python-dotenv** - Gestión de variables de entorno
- **python-decouple** - Separación de configuración del código
- **pytz** - Manejo de zonas horarias

---

## 🏗️ Arquitectura del Sistema

```
maya-learning-backend/
├── maya_backend/          # Configuración principal del proyecto Django
│   ├── settings.py       # Configuración de Django y JWT
│   ├── urls.py           # Rutas principales
│   └── wsgi.py           # Punto de entrada WSGI
│
├── usuarios/             # Aplicación de gestión de usuarios
│   ├── models.py        # Modelos de Usuario, Grupo
│   ├── views.py         # Vistas de API para usuarios
│   ├── serializers.py   # Serializers de DRF
│   ├── authentication.py # Lógica de autenticación JWT
│   ├── permissions.py   # Permisos personalizados
│   └── urls.py          # Rutas de usuarios y auth
│
├── contenido/            # Aplicación de contenido educativo
│   ├── models.py        # Modelos de Tema, Material, Vocabulario
│   ├── views.py         # Vistas de API para contenido
│   ├── serializers.py   # Serializers de contenido
│   └── urls.py          # Rutas de contenido
│
├── evaluaciones/         # Aplicación de evaluaciones
│   ├── models.py        # Modelos de Actividad, Intento, Calificación
│   ├── views.py         # Vistas de API para evaluaciones
│   ├── serializers.py   # Serializers de evaluaciones
│   └── urls.py          # Rutas de evaluaciones
│
├── reportes/             # Aplicación de generación de reportes
│   ├── models.py        # Modelo de Reporte
│   ├── views.py         # Vistas de API para reportes
│   ├── serializers.py   # Serializers de reportes
│   └── urls.py          # Rutas de reportes
│
├── requirements.txt      # Dependencias del proyecto
├── manage.py            # Script de gestión de Django
├── db.sqlite3           # Base de datos SQLite (auxiliar)
│
└── Documentación/
    ├── API_ENDPOINTS.md      # Documentación completa de endpoints
    ├── AUTENTICACION.md      # Guía de autenticación
    └── GUIA_POSTMAN.md       # Colección de Postman
```

---

## 🗄️ Modelo de Datos

### Colecciones MongoDB

#### Usuarios
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  nombre: String,
  apellido: String,
  rol: String, // "administrador" o "alumno"
  grupo_id: ObjectId, // Solo para alumnos
  nivel: String, // "Básico", "Intermedio", "Avanzado"
  activo: Boolean,
  creado_en: DateTime,
  actualizado_en: DateTime
}
```

#### Temas
```javascript
{
  _id: ObjectId,
  nombre: String, // "Números", "Comidas", "Objetos Cotidianos", "Animales"
  descripcion: String,
  orden: Number,
  activo: Boolean,
  creado_en: DateTime
}
```

#### Vocabulario
```javascript
{
  _id: ObjectId,
  tema_id: ObjectId,
  palabra_maya: String,
  palabra_espanol: String,
  pronunciacion: String,
  imagen_url: String,
  audio_url: String,
  nivel: String,
  activo: Boolean
}
```

#### Actividades
```javascript
{
  _id: ObjectId,
  tema_id: ObjectId,
  nivel: String,
  titulo: String,
  descripcion: String,
  tipo: String, // "opcion_multiple", "verdadero_falso"
  duracion_minutos: Number,
  preguntas: Array,
  puntaje_total: Number,
  activo: Boolean
}
```

#### Calificaciones
```javascript
{
  _id: ObjectId,
  alumno_id: ObjectId,
  actividad_id: ObjectId,
  intento_id: ObjectId,
  puntaje_obtenido: Number,
  puntaje_total: Number,
  porcentaje: Number,
  aprobado: Boolean,
  fecha_evaluacion: DateTime
}
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MongoDB 4.0 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/jonadev19/maya_learning_backend.git
cd maya_learning_backend
```

2. **Crear y activar entorno virtual**
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Crear un archivo `.env` en la raíz del proyecto:
```env
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True

# MongoDB
MONGO_DB_NAME=maya_learning
MONGO_HOST=localhost
MONGO_PORT=27017
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Poblar base de datos con datos de ejemplo (opcional)**
```bash
python manage.py poblar_datos
```

7. **Iniciar el servidor de desarrollo**
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000/`

---

## 📡 API Endpoints

### Autenticación

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/` | Iniciar sesión | No requerida |
| POST | `/api/auth/refresh/` | Refrescar token | No requerida |
| POST | `/api/auth/logout/` | Cerrar sesión | Requerida |
| GET | `/api/auth/me/` | Usuario actual | Requerida |

### Usuarios

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/grupos/` | Listar grupos | Autenticado |
| POST | `/api/grupos/` | Crear grupo | Admin |
| GET | `/api/administradores/` | Listar admins | Admin |
| POST | `/api/administradores/` | Crear admin | Admin |
| GET | `/api/alumnos/` | Listar alumnos | Autenticado |
| POST | `/api/alumnos/` | Crear alumno | Admin |
| GET | `/api/alumnos/<id>/` | Detalle alumno | Autenticado |
| PUT | `/api/alumnos/<id>/` | Actualizar alumno | Admin |
| DELETE | `/api/alumnos/<id>/` | Desactivar alumno | Admin |

### Contenido

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/temas/` | Listar temas | Autenticado |
| POST | `/api/temas/` | Crear tema | Admin |
| GET | `/api/materiales/` | Listar materiales | Autenticado |
| POST | `/api/materiales/` | Crear material | Admin |
| GET | `/api/vocabulario/` | Listar vocabulario | Autenticado |
| POST | `/api/vocabulario/` | Crear vocabulario | Admin |

### Evaluaciones

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/actividades/` | Listar actividades | Autenticado |
| POST | `/api/actividades/` | Crear actividad | Admin |
| POST | `/api/intentos/crear/` | Iniciar evaluación | Autenticado |
| POST | `/api/intentos/<id>/respuestas/` | Registrar respuesta | Autenticado |
| POST | `/api/intentos/<id>/finalizar/` | Finalizar evaluación | Autenticado |
| GET | `/api/calificaciones/` | Listar calificaciones | Autenticado |
| GET | `/api/calificaciones/promedio/<alumno_id>/` | Promedio alumno | Autenticado |
| GET | `/api/calificaciones/promedio-grupo/<grupo>/` | Promedio grupo | Autenticado |

### Reportes

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/reportes/` | Listar reportes | Autenticado |
| POST | `/api/reportes/` | Crear reporte | Autenticado |
| DELETE | `/api/reportes/<id>/` | Eliminar reporte | Autenticado |

**📄 Documentación completa:** Consulta [API_ENDPOINTS.md](API_ENDPOINTS.md) para ejemplos detallados de cada endpoint.

---

## 🔑 Sistema de Autenticación

### Login y obtención de tokens

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@maya.edu",
    "password": "admin123"
  }'
```

**Respuesta:**
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

### Uso de tokens en requests

```bash
curl -X GET http://localhost:8000/api/alumnos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Credenciales de Prueba

**Administrador:**
- Email: `admin@maya.edu`
- Password: `admin123`

**Alumno:**
- Email: `juan.pech@alumno.com`
- Password: `alumno123`

---

## 🧪 Testing

### Ejecutar tests
```bash
python manage.py test
```

### Probar endpoints con curl

**Listar temas:**
```bash
curl -X GET http://localhost:8000/api/temas/ \
  -H "Authorization: Bearer <tu-access-token>"
```

**Crear alumno:**
```bash
curl -X POST http://localhost:8000/api/alumnos/ \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo.alumno@alumno.com",
    "password": "password123",
    "nombre": "Nuevo",
    "apellido": "Alumno",
    "grupo_id": "507f1f77bcf86cd799439012",
    "nivel": "Básico"
  }'
```

### Testing con Postman

Importa la colección disponible en `Maya_Backend_Auth.postman_collection.json` para probar todos los endpoints.

---

## 📊 Ejemplos de Uso

### Flujo de un Alumno

1. **Login**
   ```
   POST /api/auth/login/
   ```

2. **Ver materiales disponibles**
   ```
   GET /api/materiales/?tema_id=<tema_numeros>&nivel=Básico
   ```

3. **Estudiar vocabulario**
   ```
   GET /api/vocabulario/?tema_id=<tema_numeros>&nivel=Básico
   ```

4. **Iniciar actividad**
   ```
   POST /api/intentos/crear/
   Body: { "alumno_id": "<id>", "actividad_id": "<id>" }
   ```

5. **Responder preguntas**
   ```
   POST /api/intentos/<intento_id>/respuestas/
   Body: { "pregunta_id": "<id>", "respuesta_alumno": "hun" }
   ```

6. **Finalizar y obtener calificación**
   ```
   POST /api/intentos/<intento_id>/finalizar/
   ```

### Flujo de un Administrador

1. **Ver estadísticas de grupo**
   ```
   GET /api/calificaciones/promedio-grupo/A/
   ```

2. **Generar reporte individual**
   ```
   POST /api/reportes/
   Body: {
     "tipo": "individual",
     "alumno_id": "<id>",
     "titulo": "Reporte Juan Pech"
   }
   ```

3. **Crear nuevo contenido**
   ```
   POST /api/vocabulario/
   Body: {
     "tema_id": "<id>",
     "palabra_maya": "peek'",
     "palabra_espanol": "perro",
     "nivel": "Básico"
   }
   ```

---

## 🔧 Configuración de Producción

### Variables de Entorno Recomendadas

```env
# Seguridad
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Base de Datos
MONGO_DB_NAME=maya_learning_prod
MONGO_HOST=<mongodb-host>
MONGO_PORT=27017
MONGO_USER=<usuario>
MONGO_PASSWORD=<password>

# JWT
JWT_ACCESS_LIFETIME=2  # horas
JWT_REFRESH_LIFETIME=7  # días
```

### Recomendaciones
- Usar MongoDB Atlas para base de datos en la nube
- Implementar HTTPS/SSL
- Configurar CORS apropiadamente
- Usar servidor WSGI como Gunicorn
- Implementar rate limiting
- Configurar logs y monitoreo

---

## 🚀 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Sistema de recuperación de contraseña por email
- [ ] Gamificación con puntos y insignias
- [ ] Chat en tiempo real entre alumnos y profesores
- [ ] Soporte para más tipos de actividades (fill-in-the-blank, matching)
- [ ] Exportación de reportes en Excel
- [ ] Dashboard interactivo con gráficas
- [ ] Notificaciones push para la app móvil
- [ ] Sistema de recomendación de contenido basado en rendimiento

### Mejoras Técnicas
- [ ] Implementar caché con Redis
- [ ] Agregar tests unitarios y de integración completos
- [ ] Documentación automática con Swagger/OpenAPI
- [ ] CI/CD con GitHub Actions
- [ ] Dockerización del proyecto
- [ ] API versioning
- [ ] Rate limiting avanzado
- [ ] Logging estructurado

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como parte de un sistema educativo para la preservación del lenguaje maya. Las contribuciones son bienvenidas.

### Cómo Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👨‍💻 Autor

**Jonathan**

- GitHub: [@jonadev19](https://github.com/jonadev19)
- Proyecto: [Maya Learning Backend](https://github.com/jonadev19/maya_learning_backend)

---

## 📧 Contacto

Para preguntas, sugerencias o colaboraciones, puedes contactarme a través de GitHub.

---

## 🙏 Agradecimientos

- A la comunidad maya por inspirar este proyecto
- A los educadores dedicados a preservar lenguas indígenas
- A la comunidad de Django y DRF por las excelentes herramientas

---

**⭐ Si este proyecto te resulta útil, no olvides darle una estrella en GitHub!**
