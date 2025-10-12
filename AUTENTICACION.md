# Sistema de Autenticación - Maya Backend

Este documento describe el sistema de autenticación implementado en el proyecto Maya Backend.

## Tecnologías Utilizadas

- **Django REST Framework**: Framework para crear APIs REST
- **djangorestframework-simplejwt**: Librería para autenticación con JWT (JSON Web Tokens)
- **MongoDB**: Base de datos para almacenar usuarios

## Características Implementadas

### 1. Autenticación JWT

El sistema utiliza JSON Web Tokens (JWT) para autenticar a los usuarios. JWT es un estándar de la industria que permite transmitir información de forma segura entre partes como un objeto JSON.

**Ventajas de JWT:**
- Sin estado (stateless): No requiere almacenar sesiones en el servidor
- Escalable: Funciona bien en arquitecturas distribuidas
- Seguro: Los tokens están firmados digitalmente
- Portátil: Puede usarse en diferentes dominios y aplicaciones

### 2. Tipos de Tokens

El sistema utiliza dos tipos de tokens:

- **Access Token**: Token de corta duración (2 horas) usado para autenticar peticiones
- **Refresh Token**: Token de larga duración (7 días) usado para obtener nuevos access tokens

### 3. Endpoints de Autenticación

#### Login
```
POST /api/auth/login/
```
Autentica a un usuario y retorna tokens JWT.

#### Refresh Token
```
POST /api/auth/refresh/
```
Refresca el access token usando un refresh token válido.

#### Logout
```
POST /api/auth/logout/
```
Invalida el refresh token (blacklist).

#### Usuario Actual
```
GET /api/auth/me/
```
Obtiene la información del usuario autenticado.

## Sistema de Permisos

El proyecto incluye un sistema de permisos personalizado ubicado en `usuarios/permissions.py`:

### Permisos Disponibles

1. **IsAdmin**: Solo permite acceso a usuarios con rol `administrador`
2. **IsAlumno**: Solo permite acceso a usuarios con rol `alumno`
3. **IsAdminOrReadOnly**: Permite lectura a todos los autenticados, escritura solo a administradores
4. **IsOwnerOrAdmin**: Permite acceso al propietario del recurso o a administradores

### Aplicación de Permisos

Los permisos se aplican a nivel de vista usando `permission_classes`:

```python
class GrupoListView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        # Todos los autenticados pueden leer
        ...

    def post(self, request):
        # Solo administradores pueden crear
        ...
```

## Configuración

### Settings.py

La configuración de JWT está en `maya_backend/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    ...
}
```

### Installed Apps

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    ...
]
```

## Flujo de Autenticación

### 1. Login

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

### 2. Uso del Access Token

Para acceder a endpoints protegidos, incluye el access token en el header:

```bash
curl -X GET http://localhost:8000/api/grupos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 3. Refresh del Token

Cuando el access token expira, usa el refresh token para obtener uno nuevo:

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

### 4. Logout

Para cerrar sesión, invalida el refresh token:

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

## Estructura de Archivos

```
maya-backend/
├── usuarios/
│   ├── authentication.py    # Vistas de autenticación
│   ├── permissions.py        # Permisos personalizados
│   ├── models.py            # Modelos de usuario
│   ├── serializers.py       # Serializers incluyendo LoginSerializer
│   ├── views.py             # Vistas con permisos aplicados
│   └── urls.py              # URLs de autenticación
├── maya_backend/
│   └── settings.py          # Configuración de JWT
└── API_ENDPOINTS.md         # Documentación de endpoints
```

## Seguridad

### Hash de Contraseñas

Las contraseñas se almacenan hasheadas usando el sistema de hash de Django:

```python
from django.contrib.auth.hashers import make_password, check_password

# Al crear usuario
password = make_password(password)

# Al autenticar
check_password(password_plana, password_hasheada)
```

### Blacklist de Tokens

El sistema implementa blacklist de refresh tokens para invalidarlos al hacer logout:

```python
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### Claims Personalizados

Los tokens incluyen información adicional del usuario:

```python
refresh['user_id'] = str(usuario['_id'])
refresh['email'] = usuario['email']
refresh['rol'] = usuario['rol']
refresh['nombre'] = usuario['nombre']
refresh['apellido'] = usuario['apellido']
```

## Códigos de Error Comunes

- **401 Unauthorized**: Token inválido o expirado
- **403 Forbidden**: No tienes permisos para este recurso
- **400 Bad Request**: Credenciales inválidas o parámetros faltantes

## Pruebas Manuales

### Crear un administrador

```bash
curl -X POST http://localhost:8000/api/administradores/ \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@admin.com",
    "password": "password123",
    "nombre": "Nuevo",
    "apellido": "Admin"
  }'
```

### Verificar permisos

Intenta acceder a un endpoint protegido sin token:
```bash
curl -X GET http://localhost:8000/api/grupos/
# Debe retornar 401 Unauthorized
```

Con token de alumno intentando crear un grupo:
```bash
curl -X POST http://localhost:8000/api/grupos/ \
  -H "Authorization: Bearer <token-alumno>" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "C", "descripcion": "Test"}'
# Debe retornar 403 Forbidden
```

## Mejoras Futuras

1. **Rate Limiting**: Limitar intentos de login por IP
2. **Refresh Token Rotation**: Implementar rotación automática de refresh tokens
3. **Password Reset**: Sistema de recuperación de contraseña
4. **Two-Factor Authentication**: Autenticación de dos factores
5. **OAuth2**: Integración con proveedores externos (Google, Facebook, etc.)

## Recursos

- [Documentación Django REST Framework](https://www.django-rest-framework.org/)
- [Documentación Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decodificador de tokens JWT
- [Documentación API Completa](./API_ENDPOINTS.md)