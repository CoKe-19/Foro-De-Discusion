# Evaluación N°2 – Desarrollo Django CRUD (con Login)

## 0) Objetivo General
Construir una aplicación web tipo Foro de Discusión con autenticación obligatoria y CRUD completo para tres modelos relacionados: Hilo, Respuesta y Categoría. Se documenta casos de uso y diseño de datos.

## 1) Entorno / Versiones
- Python: 3.11
- Django: 5.2.5
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

## 3) Acceso y CRUD
- Login: /login/
- Logout: /logout/
- Hilos (Entidad A):
  - Crear: /hilos/crear/
  - Listar: /hilos/
  - Editar: /hilos/<hilo_id>/editar/
  - Eliminar: /hilos/<hilo_id>/eliminar/
- Respuestas (Entidad B):
  - Crear: dentro de /hilos/<hilo_id>/detalle/
  - Editar: /respuestas/<respuesta_id>/editar/
  - Eliminar: /respuestas/<respuesta_id>/eliminar/
- Categorías (Entidad C):
  - Crear: /categorias/crear/
  - Listar: /categorias/
  - Editar: /categorias/<categoria_id>/editar/
  - Eliminar: /categorias/<categoria_id>/eliminar/

Notas importantes:
- Las vistas de crear/editar/eliminar requieren login.
- Mensajes de éxito/error visibles con messages.
- Formularios con validaciones de campos obligatorios y tipos correctos.
- Intento de eliminar categoría con hilos asociados muestra mensaje de error y no se elimina.

## 4) Casos de Uso

### CU1: Gestión Hilos
**Actores:** Usuario, Administrador  
**Precondiciones:** Usuario autenticado; administrador con permisos de staff; para editar/eliminar, el hilo debe pertenecer al usuario o el usuario debe ser admin.  
**Flujo principal:**
1. Usuario inicia sesión y selecciona “Crear Hilo”.
2. Ingresa título, contenido y categoría; sistema valida y guarda.
3. Usuario puede ver hilos generales o propios.
4. Usuario edita/elimina sus hilos.
5. Administrador puede ver, editar o eliminar cualquier hilo.  
**Excepciones/Errores:**
- Campos obligatorios vacíos → mensaje de error.
- Intento de editar/eliminar hilo ajeno → acceso denegado.
- Admin sin permisos → acceso denegado.  
**Postcondiciones:** Hilo creado, editado o eliminado correctamente; lista de hilos actualizada; se muestran mensajes de éxito o error.

### CU2: Gestión Categorías
**Actores:** Administrador  
**Precondiciones:** Usuario autenticado con permisos de staff.  
**Flujo principal:**
1. Administrador crea una nueva categoría usando el formulario.
2. Administrador puede editar el nombre de categorías existentes.
3. Administrador puede listar todas las categorías.
4. Administrador puede eliminar categorías sin hilos asociados.  
**Excepciones/Errores:**
- Campos obligatorios vacíos → mensaje de error.
- Intento de editar/eliminar categoría sin permisos → acceso denegado.
- Intento de eliminar categoría con hilos asociados → mensaje de error, no se elimina.  
**Postcondiciones:** Categoría creada, editada o eliminada correctamente; lista de categorías actualizada.

### CU3: Gestión Respuestas
**Actores:** Usuario, Administrador  
**Precondiciones:** Usuario autenticado; la respuesta pertenece al usuario o el usuario es admin.  
**Flujo principal:**
1. Usuario selecciona un hilo y escribe una respuesta.
2. Sistema valida y guarda la respuesta.
3. Usuario puede editar o eliminar sus respuestas.
4. Administrador puede eliminar cualquier respuesta.  
**Excepciones/Errores:**
- Campos obligatorios vacíos → mensaje de error.
- Intento de editar/eliminar respuesta ajena → acceso denegado.  
**Postcondiciones:** Respuesta creada, editada o eliminada correctamente; lista de respuestas actualizada.

## 5) Diagrama de Clases
- Clases: User (Django), Hilo, Respuesta, Categoria  
- Relaciones:
  - User 1 → 0..* Hilo (crea)
  - User 1 → 0..* Respuesta (publica)
  - Categoria 1 → 0..* Hilo (contiene)
  - Hilo 1 → 0..* Respuesta (recibe)
- Claves primarias, foráneas y cardinalidades definidas.  
- Validaciones y permisos según modelo.

## 6) Recomendaciones / Notas
- Login obligatorio para operaciones sensibles.  
- CSRF en todos los formularios.  
- Mensajes flash para feedback (success/error).  
- on_delete definido en todas las FK (PROTECT o CASCADE según corresponda).  
- Estructura de carpetas: proyecto/, hilos/, templates/, static/.  
- CSS simple y consistente.  

## 7) Comandos Clave
python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver

## 8) Observaciones
- Las vistas de listado pueden ser públicas o privadas según diseño; mínimo uno requiere login.  
- Intento de borrar categoría con hilos asociados no genera error de servidor, solo mensaje al usuario.  
- Todos los formularios reutilizan form.html, excepto login que usa plantilla propia de Django.  
- El proyecto cumple con la rúbrica: 3 CRUD completos, validaciones, permisos y mensajes de feedback.
