# BiblioApp — Sistema de Gestión de Biblioteca

Proyecto web desarrollado con **Python + Django** como Trabajo Práctico Final.  
Permite gestionar una biblioteca pequeña: autores, libros y préstamos, con sistema de autenticación de usuarios.

---

## Cómo correr el proyecto

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd web-python-django
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario (administrador)
```bash
python manage.py createsuperuser
```
> Sugerencia de credenciales para prueba:
> - **Usuario:** `admin`
> - **Email:** (puede dejarse vacío)
> - **Contraseña:** `admin1234`

### 6. Correr el servidor
```bash
python manage.py runserver
```

Ingresar a: **http://127.0.0.1:8000**

---

## Cómo probar los distintos roles

### 👁️ Como visitante (sin cuenta)
- Ingresá a **http://127.0.0.1:8000** sin iniciar sesión
- Podés ver la lista de libros, autores y préstamos
- **No verás** los botones de Agregar / Editar / Eliminar
- Si intentás ingresar a una URL protegida, el sistema te redirige al Login

### 👤 Como usuario registrado (sin permisos de staff)
**Crear cuenta nueva:**
1. Hacé clic en **Registrarse** en el navbar
2. Completá usuario, email y contraseña
3. Accedés automáticamente

**Un usuario registrado puede:**
- Ver el detalle de cada libro (vista protegida con `LoginRequiredMixin`)
- Ver y editar su propio perfil (`/accounts/perfil/`)
- Cambiar su contraseña

**No puede:** agregar, editar ni eliminar libros/autores/préstamos

### 🔐 Como staff / administrador
Usar las credenciales del superusuario creado en el paso 5 (`admin` / `admin1234`).

**El staff puede hacer todo lo anterior más:**
- Agregar, editar y eliminar autores y libros
- Registrar préstamos y marcar devoluciones
- Acceder al panel de administración en `/admin/`

### 🚪 Logout
Al cerrar sesión desde el menú del navbar, el sistema redirige automáticamente al **home**.

---

## Orden para probar las funcionalidades

1. **Agregar un Autor** → desde el navbar `Autores`  
   `http://127.0.0.1:8000/autores/agregar/`

2. **Agregar un Libro** → requiere tener al menos un autor cargado  
   `http://127.0.0.1:8000/libros/agregar/`

3. **Registrar un Préstamo** → requiere tener al menos un libro cargado  
   `http://127.0.0.1:8000/prestamos/registrar/`

4. **Marcar devolución** → desde la lista de préstamos o el detalle del libro

5. **Buscar un libro** → por título o nombre de autor  
   `http://127.0.0.1:8000/libros/buscar/`

---

## Estructura del proyecto

```
web-python-django/
  Biblioteca/        → configuración del proyecto (settings, urls)
  catalogo/          → app principal: libros, autores, préstamos
    models.py        → modelos: Autor, Libro, Prestamo
    views.py         → vistas FBV con @login_required y CBV con LoginRequiredMixin
    forms.py         → formularios para insertar y buscar datos
    urls.py          → rutas de la app
    templates/
      base.html               → template base (herencia)
      catalogo/
        index.html            → home con estadísticas y libros disponibles
        autores_lista.html    → lista de autores
        autor_form.html       → formulario agregar/editar autor
        autor_detalle.html    → detalle del autor con sus libros
        libros_lista.html     → lista de libros
        libro_form.html       → formulario agregar/editar libro
        libro_detalle.html    → detalle del libro con préstamos activos
        prestamos_lista.html  → lista de préstamos
        prestamo_form.html    → formulario registrar préstamo
        buscar.html           → buscador de libros
        confirmar_eliminar.html → confirmación antes de eliminar
        about.html            → página sobre la autora
  accounts/          → app de autenticación y perfiles
    models.py        → modelo Perfil (OneToOne con User)
    views.py         → login, logout, signup, perfil, cambiar contraseña
    forms.py         → formularios de registro, edición de perfil y contraseña
    urls.py          → rutas de autenticación
    templates/
      accounts/
        login.html            → formulario de inicio de sesión
        signup.html           → formulario de registro
        perfil.html           → vista del perfil del usuario
        perfil_editar.html    → edición de perfil y avatar
        cambiar_password.html → cambio de contraseña
```

---

## Modelos

- **Autor** — nombre, país, año de nacimiento
- **Libro** — título, ISBN, número de catálogo (único), año de publicación, fecha de ingreso, cantidad disponible, imagen de portada (opcional), FK a Autor
- **Prestamo** — fecha de préstamo, fecha de devolución, FK a Libro, nombre del usuario, estado devuelto
- **Perfil** — OneToOne con User, avatar (opcional), biografía

---

## Tecnologías

- Python 3 + Django
- Bootstrap 5 + Bootstrap Icons
- SQLite (base de datos de desarrollo)
- Pillow (manejo de imágenes)
