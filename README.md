# Foro de Discusión - Proyecto Django

## 0) Objetivo General
Construir una aplicación web tipo Foro de Discusión con autenticación obligatoria y CRUD completo para los modelos Hilo, Respuesta, Categoría, Perfil y Likes. Incluye validaciones, permisos, filtros, búsqueda y documentación de la API REST.

## 1) Entorno / Versiones
- Python: 3.11
- Django: 5.2.5
- Django REST Framework: según requirements.txt
- Base de datos: SQLite

## 2) Instalación
1. Crear entorno virtual:
python -m venv venv
2. Activar entorno:
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
3. Instalar dependencias:
pip install -r requirements.txt
4. Migrar base de datos:
python manage.py migrate
5. Crear superusuario:
python manage.py createsuperuser
6. Ejecutar servidor:
python manage.py runserver

## 3) Acceso Web y CRUD
### Login / Logout
- Login: /login/
- Logout: /logout/

### Hilos
- Crear: /hilos/crear/
- Listar: /hilos/
- Editar: /hilos/<hilo_id>/editar/
- Eliminar: /hilos/<hilo_id>/eliminar/

### Respuestas
- Crear: desde /hilos/<hilo_id>/detalle/
- Editar: /respuestas/<respuesta_id>/editar/
- Eliminar: /respuestas/<respuesta_id>/eliminar/

### Categorías
- Crear: /categorias/crear/
- Listar: /categorias/
- Editar: /categorias/<categoria_id>/editar/
- Eliminar: /categorias/<categoria_id>/eliminar/ (solo si no tiene hilos)

### Perfil
- Ver: /perfil/
- Editar: /perfil/editar/

### Likes
- Dar/Quitar like: integrado en detalle de hilo y respuestas

Notas importantes:
- Crear/Editar/Eliminar requiere login.
- Mensajes de éxito/error visibles con messages.
- Validaciones de campos obligatorios y formatos correctos.
- Intento de borrar categoría con hilos asociados muestra mensaje y no elimina.

## 4) Casos de Uso
### CU1: Gestión de Hilos
- Actores: Usuario, Administrador
- Precondiciones: Usuario autenticado; administrador con permisos staff.
- Flujo principal: Crear, editar, eliminar hilos. Ver lista de hilos generales o propios.
- Excepciones: Campos vacíos → mensaje de error. Editar/eliminar hilo ajeno → acceso denegado.
- Postcondición: Hilo creado/actualizado/eliminado correctamente.

### CU2: Gestión de Categorías
- Actor: Administrador
- Precondiciones: Usuario autenticado con permisos staff
- Flujo principal: Crear, editar, listar categorías. Eliminar solo si no tiene hilos asociados.
- Excepciones: Campos vacíos → error. Editar/eliminar categoría con hilos → error.
- Postcondición: Categoría gestionada correctamente.

### CU3: Gestión de Respuestas
- Actores: Usuario, Administrador
- Precondiciones: Usuario autenticado; la respuesta pertenece al usuario o es admin
- Flujo principal: Crear, editar, eliminar respuestas
- Excepciones: Campos obligatorios vacíos → mensaje. Editar/eliminar respuesta ajena → acceso denegado
- Postcondición: Respuesta gestionada correctamente

### CU4: Gestión de Perfil
- Actores: Usuario (incluye administradores como usuarios normales)
- Precondiciones: Usuario autenticado; el perfil debe pertenecer al usuario
- Flujo principal: Acceder a la sección Perfil, ver información (avatar, apodo, bio, ubicación, email, estadísticas), editar datos y actualizar foto, apodo, bio o ubicación; sistema valida y guarda cambios
- Excepciones: Campos vacíos → mensaje de error; datos inválidos → mensaje de error
- Postcondición: Perfil actualizado correctamente; cambios reflejados en base de datos; mensajes de éxito o error mostrados

### CU5: Gestión de Likes en Respuestas
- Actores: Usuario
- Precondiciones: Usuario autenticado; la respuesta debe existir
- Flujo principal: Acceder a un hilo y sus respuestas, dar like a una respuesta (registrar en DB), si ya existe like puede quitarlo; sistema actualiza contador de likes en tiempo real
- Excepciones: Usuario no autenticado → acceso denegado; intentar quitar like inexistente → mensaje de error
- Postcondición: Like registrado o quitado correctamente; contador de likes actualizado; mensajes de éxito o error mostrados

## 5) Diagrama de Clases
- Modelos: User (Django), Hilo, Respuesta, Categoria, Perfil, Like
- Relaciones: User 1 → N Hilo, User 1 → N Respuesta, Categoria 1 → N Hilo, Hilo 1 → N Respuesta
- Claves foráneas y cardinalidades definidas en modelos.
- Validaciones y permisos según modelo.

## 6) Permisos y Flujo de Acceso (Diagrama Textual)
Usuarios autenticados (no admin) -> GET Hilos / Respuestas / Categorías : PERMITIDO  
Usuarios autenticados (no admin) -> POST/PUT/DELETE Hilos / Respuestas / Categorías : DENEGADO  
Administradores -> CRUD completo Hilos / Respuestas / Categorías : PERMITIDO  
Usuario -> GET/PUT Perfil propio : PERMITIDO  
Usuario -> Dar/Quitar Likes en Respuestas : PERMITIDO  
Usuario -> Editar Perfil ajeno / Dar Likes a respuesta no existente : DENEGADO  
Usuarios no autenticados -> Cualquier acción sensible : DENEGADO (401)

## 7) Recomendaciones / Notas
- Login obligatorio para operaciones sensibles.
- CSRF en todos los formularios.
- Mensajes flash (success / error) para feedback.
- on_delete definido para todas las FK (PROTECT o CASCADE).
- Estructura de carpetas:
  proyecto/
    settings.py
    urls.py
    wsgi.py
  hilos/
    models.py
    serializers.py
    views_api.py
    api_urls.py
    templates/
    static/
- CSS simple y consistente.

## 8) Comandos Clave
python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver

## 9) API REST (Django REST Framework)
### Autenticación
- JWT: /api/token/ (obtener access y refresh)  
- JWT refresh: /api/token/refresh/  
- También soporta TokenAuthentication o sesión de Django

### Endpoints Principales
Hilo: /api/hilos/ → GET Listar (todos los usuarios), POST Crear (solo admin), GET /<id>/ detalle, PUT/PATCH /<id>/ editar (solo admin), DELETE /<id>/ eliminar (solo admin), PUT /<id>/cambiar-categoria/ cambiar categoría  
Respuesta: /api/respuestas/ → GET Listar (todos los usuarios), POST Crear (solo admin), GET /<id>/ detalle, PUT/PATCH /<id>/ editar (solo admin), DELETE /<id>/ eliminar (solo admin)  
Categoría: /api/categorias/ → GET Listar (todos los usuarios), POST Crear (solo admin), GET /<id>/ detalle, PUT/PATCH /<id>/ editar (solo admin), DELETE /<id>/ eliminar solo si no tiene hilos  
Perfil: /api/perfil/ → GET ver (usuario propio), PUT/PATCH editar (usuario propio)  
Likes: /api/likes/ → POST dar/quitar like a respuesta (usuario autenticado)

### Filtros, búsqueda y ordenamiento
- Filtros por campo: filterset_fields
- Búsqueda: search_fields
- Ordenamiento: ordering_fields
- Paginación: PageNumberPagination (10 items por página)

## 10) Ejemplo de Pruebas API con Thunder Client
**Header para requests protegidos:**  
Authorization: Bearer <access_token>  
Content-Type: application/json  

**Tabla de CRUD y permisos**
| Recurso | Método | Usuario no admin | Admin | Resultado esperado |  
|---------|--------|-----------------|-------|------------------|  
| /api/hilos/ | GET | ✅ | ✅ | Solo usuarios autenticados pueden ver |  
| /api/hilos/ | POST | ❌ | ✅ | Solo admin puede crear |  
| /api/hilos/<id>/ | PUT/PATCH | ❌ | ✅ | Solo admin puede editar |  
| /api/hilos/<id>/ | DELETE | ❌ | ✅ | Solo admin puede eliminar |  
| /api/respuestas/ | GET | ✅ | ✅ | Listado permitido |  
| /api/respuestas/ | POST | ❌ | ✅ | Solo admin puede crear |  
| /api/categorias/ | GET | ✅ | ✅ | Listado permitido |  
| /api/categorias/ | POST/PUT/DELETE | ❌ | ✅ | Solo admin; DELETE falla si tiene hilos |  
| /api/perfil/ | GET/PUT | ✅ Solo propio | ✅ Solo propio | Usuario gestiona su perfil |  
| /api/likes/ | POST | ✅ | ✅ | Dar/quitar like permitido para usuarios autenticados |  

**Ejemplo POST Hilo**  
POST http://localhost:8000/api/hilos/  
Body:  
{  
  "titulo": "Ejemplo de Hilo",  
  "contenido": "Contenido de prueba",  
  "categoria": 1,  
  "usuario": 1  
}  
Respuesta: `201 Created` si es admin, `403 Forbidden` si no es admin

## 11) Documentación
- Schema OpenAPI: /api/schema/  
- Swagger UI: /api/docs/

## 12) Observaciones finales
- Usuarios autenticados → GET permitido, POST/PUT/DELETE solo admins (para hilos, respuestas, categorías)  
- Usuario puede ver/editar su propio perfil y dar/quitar likes en respuestas  
- Intentos de acciones no permitidas devuelven códigos HTTP correctos (401, 403, 400, 404)  
- Proyecto cumple con la rúbrica de evaluación 3: CRUD completo, validaciones, filtros, búsqueda, ordenamiento, paginación, permisos, JWT, documentación OpenAPI, manejo correcto de errores
