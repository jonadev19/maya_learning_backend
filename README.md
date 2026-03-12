# 🌟 Maya Learning - Backend API

> Backend system for a mobile application for teaching the Maya language, with user management, educational content, assessments, and report generation.

![Django](https://img.shields.io/badge/Django-5.2.7-green?style=flat&logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16.1-red?style=flat)
![MongoDB](https://img.shields.io/badge/MongoDB-3.11.4-green?style=flat&logo=mongodb)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)

---

## 📖 Project Description

**Maya Learning Backend** is a REST API built with Django and Django REST Framework that serves as the backend for an educational mobile application dedicated to teaching the Maya language. The system manages users (administrators and students), educational content organized by topics and levels, assessment activities, and PDF report generation.

### Educational Context

The project addresses the need to preserve and teach the Maya language through a modern digital platform. Content is organized into four main topics:
- 🔢 **Numbers** - Numbers from 0 to 100 in Maya
- 🍽️ **Foods** - Traditional food vocabulary
- 🏠 **Everyday Objects** - Day-to-day items
- 🦎 **Animals** - Local and regional fauna

---

## ✨ Key Features

### 🔐 Authentication System
- JWT (JSON Web Tokens) authentication with access and refresh tokens
- Role-based permission system (Administrator/Student)
- Secure password management with hashing
- Token blacklist for secure logout

### 👥 User Management
- **Administrators**: Teachers with full permissions
  - Create, update, and deactivate users
  - Manage educational content
  - Generate individual and group reports
  - View grades and statistics

- **Students**: Learners with controlled access
  - Access educational materials
  - Complete activities and assessments
  - View personal progress
  - Organized by groups (A, B) and levels (Basic, Intermediate, Advanced)

### 📚 Educational Content
- **Topics**: Organizational structure for content
- **Materials**: Educational resources with multimedia support
- **Vocabulary**: Database of Maya words with translations, pronunciation, and audiovisual resources

### 📝 Assessment System
- **Activities**: Configurable quizzes and exercises
- **Questions**: Support for multiple types (multiple choice, true/false)
- **Attempts**: Detailed record of each assessment attempt
- **Grades**: Automatic grading system with average calculation

### 📊 Reports and Statistics
- Individual reports per student
- Group reports
- Statistics by topic
- PDF file generation
- Average and pass rate calculations

---

## 🛠️ Technologies Used

### Backend Framework
- **Django 5.2.7** - High-level web framework
- **Django REST Framework 3.16.1** - Toolkit for building REST APIs

### Database
- **MongoDB 3.11.4** - Document-oriented NoSQL database
- **PyMongo** - Official Python driver for MongoDB

### Authentication and Security
- **djangorestframework-simplejwt 5.5.1** - JWT authentication
- **PyJWT 2.10.1** - JWT token library
- **Django password hashing** - Secure password hashing system

### Additional Tools
- **python-dotenv** - Environment variable management
- **python-decouple** - Configuration separation from code
- **pytz** - Timezone handling

---

## 🏗️ System Architecture

```
maya-learning-backend/
├── maya_backend/          # Main Django project configuration
│   ├── settings.py       # Django and JWT configuration
│   ├── urls.py           # Main routes
│   └── wsgi.py           # WSGI entry point
│
├── usuarios/             # User management application
│   ├── models.py        # User, Group models
│   ├── views.py         # API views for users
│   ├── serializers.py   # DRF serializers
│   ├── authentication.py # JWT authentication logic
│   ├── permissions.py   # Custom permissions
│   └── urls.py          # User and auth routes
│
├── contenido/            # Educational content application
│   ├── models.py        # Topic, Material, Vocabulary models
│   ├── views.py         # API views for content
│   ├── serializers.py   # Content serializers
│   └── urls.py          # Content routes
│
├── evaluaciones/         # Assessments application
│   ├── models.py        # Activity, Attempt, Grade models
│   ├── views.py         # API views for assessments
│   ├── serializers.py   # Assessment serializers
│   └── urls.py          # Assessment routes
│
├── reportes/             # Report generation application
│   ├── models.py        # Report model
│   ├── views.py         # API views for reports
│   ├── serializers.py   # Report serializers
│   └── urls.py          # Report routes
│
├── requirements.txt      # Project dependencies
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database (auxiliary)
│
└── Documentacion/
    ├── API_ENDPOINTS.md      # Complete endpoint documentation
    ├── AUTENTICACION.md      # Authentication guide
    └── GUIA_POSTMAN.md       # Postman collection
```

---

## 🗄️ Data Model

### MongoDB Collections

#### Users
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  nombre: String,
  apellido: String,
  rol: String, // "administrador" or "alumno"
  grupo_id: ObjectId, // Students only
  nivel: String, // "Básico", "Intermedio", "Avanzado"
  activo: Boolean,
  creado_en: DateTime,
  actualizado_en: DateTime
}
```

#### Topics
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

#### Vocabulary
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

#### Activities
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

#### Grades
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

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB 4.0 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/jonadev19/maya_learning_backend.git
cd maya_learning_backend
```

2. **Create and activate virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# MongoDB
MONGO_DB_NAME=maya_learning
MONGO_HOST=localhost
MONGO_PORT=27017
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Populate database with sample data (optional)**
```bash
python manage.py poblar_datos
```

7. **Start the development server**
```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000/`

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/auth/login/` | Log in | Not required |
| POST | `/api/auth/refresh/` | Refresh token | Not required |
| POST | `/api/auth/logout/` | Log out | Required |
| GET | `/api/auth/me/` | Current user | Required |

### Users

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/api/grupos/` | List groups | Authenticated |
| POST | `/api/grupos/` | Create group | Admin |
| GET | `/api/administradores/` | List admins | Admin |
| POST | `/api/administradores/` | Create admin | Admin |
| GET | `/api/alumnos/` | List students | Authenticated |
| POST | `/api/alumnos/` | Create student | Admin |
| GET | `/api/alumnos/<id>/` | Student detail | Authenticated |
| PUT | `/api/alumnos/<id>/` | Update student | Admin |
| DELETE | `/api/alumnos/<id>/` | Deactivate student | Admin |

### Content

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/api/temas/` | List topics | Authenticated |
| POST | `/api/temas/` | Create topic | Admin |
| GET | `/api/materiales/` | List materials | Authenticated |
| POST | `/api/materiales/` | Create material | Admin |
| GET | `/api/vocabulario/` | List vocabulary | Authenticated |
| POST | `/api/vocabulario/` | Create vocabulary | Admin |

### Assessments

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/api/actividades/` | List activities | Authenticated |
| POST | `/api/actividades/` | Create activity | Admin |
| POST | `/api/intentos/crear/` | Start assessment | Authenticated |
| POST | `/api/intentos/<id>/respuestas/` | Submit answer | Authenticated |
| POST | `/api/intentos/<id>/finalizar/` | Finish assessment | Authenticated |
| GET | `/api/calificaciones/` | List grades | Authenticated |
| GET | `/api/calificaciones/promedio/<alumno_id>/` | Student average | Authenticated |
| GET | `/api/calificaciones/promedio-grupo/<grupo>/` | Group average | Authenticated |

### Reports

| Method | Endpoint | Description | Permissions |
|--------|----------|-------------|-------------|
| GET | `/api/reportes/` | List reports | Authenticated |
| POST | `/api/reportes/` | Create report | Authenticated |
| DELETE | `/api/reportes/<id>/` | Delete report | Authenticated |

**📄 Full documentation:** See [API_ENDPOINTS.md](API_ENDPOINTS.md) for detailed examples of each endpoint.

---

## 🔑 Authentication System

### Login and token retrieval

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@maya.edu",
    "password": "admin123"
  }'
```

**Response:**
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

### Using tokens in requests

```bash
curl -X GET http://localhost:8000/api/alumnos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Test Credentials

**Administrator:**
- Email: `admin@maya.edu`
- Password: `admin123`

**Student:**
- Email: `juan.pech@alumno.com`
- Password: `alumno123`

---

## 🧪 Testing

### Run tests
```bash
python manage.py test
```

### Test endpoints with curl

**List topics:**
```bash
curl -X GET http://localhost:8000/api/temas/ \
  -H "Authorization: Bearer <your-access-token>"
```

**Create student:**
```bash
curl -X POST http://localhost:8000/api/alumnos/ \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "new.student@alumno.com",
    "password": "password123",
    "nombre": "New",
    "apellido": "Student",
    "grupo_id": "507f1f77bcf86cd799439012",
    "nivel": "Básico"
  }'
```

### Testing with Postman

Import the collection available at `Maya_Backend_Auth.postman_collection.json` to test all endpoints.

---

## 📊 Usage Examples

### Student Flow

1. **Login**
   ```
   POST /api/auth/login/
   ```

2. **View available materials**
   ```
   GET /api/materiales/?tema_id=<numbers_topic>&nivel=Básico
   ```

3. **Study vocabulary**
   ```
   GET /api/vocabulario/?tema_id=<numbers_topic>&nivel=Básico
   ```

4. **Start activity**
   ```
   POST /api/intentos/crear/
   Body: { "alumno_id": "<id>", "actividad_id": "<id>" }
   ```

5. **Answer questions**
   ```
   POST /api/intentos/<intento_id>/respuestas/
   Body: { "pregunta_id": "<id>", "respuesta_alumno": "hun" }
   ```

6. **Finish and get grade**
   ```
   POST /api/intentos/<intento_id>/finalizar/
   ```

### Administrator Flow

1. **View group statistics**
   ```
   GET /api/calificaciones/promedio-grupo/A/
   ```

2. **Generate individual report**
   ```
   POST /api/reportes/
   Body: {
     "tipo": "individual",
     "alumno_id": "<id>",
     "titulo": "Report Juan Pech"
   }
   ```

3. **Create new content**
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

## 🔧 Production Configuration

### Recommended Environment Variables

```env
# Security
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
MONGO_DB_NAME=maya_learning_prod
MONGO_HOST=<mongodb-host>
MONGO_PORT=27017
MONGO_USER=<user>
MONGO_PASSWORD=<password>

# JWT
JWT_ACCESS_LIFETIME=2  # hours
JWT_REFRESH_LIFETIME=7  # days
```

### Recommendations
- Use MongoDB Atlas for cloud database
- Implement HTTPS/SSL
- Configure CORS appropriately
- Use a WSGI server like Gunicorn
- Implement rate limiting
- Configure logging and monitoring

---

## 🤝 Contributions

This project was developed as part of an educational system for the preservation of the Maya language. Contributions are welcome.

### How to Contribute
1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT license.

---

## 👨‍💻 Author

**Jonathan**

- GitHub: [@jonadev19](https://github.com/jonadev19)
- Project: [Maya Learning Backend](https://github.com/jonadev19/maya_learning_backend)

---

## 📧 Contact

For questions, suggestions, or collaborations, feel free to reach out through GitHub.

---

## 🙏 Acknowledgements

- To the Maya community for inspiring this project
- To the educators dedicated to preserving indigenous languages
- To the Django and DRF community for the excellent tools

---

**⭐ If you find this project useful, don't forget to give it a star on GitHub!**
