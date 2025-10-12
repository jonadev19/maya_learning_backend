# Guía para Testear Autenticación con Postman

## Paso 1: Importar la Colección

1. Abre Postman
2. Click en **Import** (esquina superior izquierda)
3. Selecciona el archivo `Maya_Backend_Auth.postman_collection.json`
4. Click en **Import**

## Paso 2: Iniciar el Servidor

Antes de testear, asegúrate de que el servidor esté corriendo:

```bash
cd /Users/jonathan/Desktop/dev/maya-backend
python manage.py runserver
```

## Paso 3: Pruebas Paso a Paso

### ✅ Prueba 1: Login como Administrador

1. En Postman, abre la carpeta **Autenticación**
2. Selecciona **"1. Login - Administrador"**
3. Verifica que el body tenga:
   ```json
   {
     "email": "admin@maya.edu",
     "password": "admin123"
   }
   ```
4. Click en **Send**

**Resultado esperado (200 OK):**
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

**Los tokens se guardan automáticamente** como variables de entorno.

---

### ✅ Prueba 2: Acceder a Endpoint SIN Token (Debe Fallar)

1. Selecciona **"Listar Grupos (Sin Auth - Debe Fallar)"**
2. Verifica que NO tenga Authorization header
3. Click en **Send**

**Resultado esperado (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### ✅ Prueba 3: Acceder a Endpoint CON Token

1. Selecciona **"Listar Grupos (Con Auth)"**
2. Ve a la pestaña **Authorization**
3. Verifica que esté configurado como **Bearer Token** con `{{access_token}}`
4. Click en **Send**

**Resultado esperado (200 OK):**
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

---

### ✅ Prueba 4: Obtener Usuario Actual

1. Selecciona **"3. Obtener Usuario Actual (Me)"**
2. Click en **Send**

**Resultado esperado (200 OK):**
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

### ✅ Prueba 5: Crear Grupo como Administrador

1. Selecciona **"Crear Grupo (Admin)"**
2. Verifica el body:
   ```json
   {
     "nombre": "C",
     "descripcion": "Grupo C - Turno vespertino"
   }
   ```
3. Click en **Send**

**Resultado esperado (201 CREATED):**
```json
{
  "id": "507f1f77bcf86cd799439099",
  "nombre": "C",
  "descripcion": "Grupo C - Turno vespertino",
  "activo": true,
  "creado_en": "2025-10-12T20:00:00Z",
  "actualizado_en": "2025-10-12T20:00:00Z"
}
```

---

### ✅ Prueba 6: Login como Alumno

1. Selecciona **"2. Login - Alumno"**
2. Click en **Send**

Esto guardará los tokens del alumno en variables separadas.

---

### ✅ Prueba 7: Intentar Crear Grupo como Alumno (Debe Fallar)

1. Selecciona **"Crear Grupo (Alumno - Debe Fallar)"**
2. Este request usa `{{access_token_alumno}}`
3. Click en **Send**

**Resultado esperado (403 Forbidden):**
```json
{
  "detail": "Solo los administradores pueden modificar este recurso"
}
```

---

### ✅ Prueba 8: Refresh Token

1. Selecciona **"4. Refresh Token"**
2. Click en **Send**

**Resultado esperado (200 OK):**
```json
{
  "access": "nuevo_access_token...",
  "refresh": "nuevo_refresh_token..."
}
```

Los nuevos tokens se guardan automáticamente.

---

### ✅ Prueba 9: Logout

1. Selecciona **"5. Logout"**
2. Click en **Send**

**Resultado esperado (200 OK):**
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

---

### ✅ Prueba 10: Intentar Usar Token Después del Logout

1. Intenta usar **"4. Refresh Token"** nuevamente
2. Debería fallar porque el token está en blacklist

**Resultado esperado (401 Unauthorized):**
```json
{
  "error": "Token inválido o expirado"
}
```

---

## Configuración Manual (Si no usas la colección)

### Para cualquier request con autenticación:

1. Ve a la pestaña **Authorization**
2. Selecciona **Type: Bearer Token**
3. En **Token** pega tu access token
4. O usa la variable: `{{access_token}}`

### Ejemplo de Request Manual:

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "email": "admin@maya.edu",
  "password": "admin123"
}
```

---

## Variables de Entorno en Postman

La colección usa estas variables (se guardan automáticamente):

| Variable | Descripción |
|----------|-------------|
| `base_url` | http://localhost:8000/api |
| `access_token` | Token de acceso del admin |
| `refresh_token` | Token de refresco del admin |
| `access_token_alumno` | Token de acceso del alumno |
| `refresh_token_alumno` | Token de refresco del alumno |
| `user_id` | ID del usuario autenticado |

Para ver/editar variables:
1. Click en el ícono del ojo (👁️) en la esquina superior derecha
2. O click en **Environments** en la barra lateral

---

## Solución de Problemas

### Error: "Connection refused"
- Verifica que el servidor esté corriendo en el puerto 8000
- Comando: `python manage.py runserver`

### Error: "Authentication credentials were not provided"
- El token no está en el header
- Verifica que tengas el header: `Authorization: Bearer <token>`

### Error: "Token is invalid or expired"
- El access token expiró (2 horas)
- Usa el endpoint de **Refresh Token**
- O haz login nuevamente

### Error: "Credenciales inválidas"
- Verifica email y password
- Asegúrate de que existan usuarios en la base de datos
- Ejecuta: `python manage.py poblar_datos` (si existe)

### Error de MongoDB
- Verifica que MongoDB Atlas esté conectado
- Revisa las credenciales en el archivo `.env`

---

## Próximos Pasos

Una vez que todo funcione:

1. ✅ Testea todos los endpoints de la carpeta **Usuarios**
2. ✅ Testea diferentes roles (admin vs alumno)
3. ✅ Verifica los permisos de cada endpoint
4. ✅ Prueba el flujo completo: login → usar API → logout

---

## Tips de Postman

- Usa **Collections** para organizar tus requests
- Usa **Variables** para no repetir tokens
- Usa **Tests** (Scripts) para validación automática
- Guarda ejemplos de respuestas exitosas
- Crea un **Environment** para desarrollo y otro para producción