# BiblioApp — Sistema de Gestión de Biblioteca

Proyecto web desarrollado con **Python + Django** como parte del TP3.  
Permite gestionar una biblioteca pequeña: autores, libros y préstamos.

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

### 5. Correr el servidor
```bash
python manage.py runserver
```

Ingresar a: **http://127.0.0.1:8000**

---

## Orden para probar las funcionalidades

1. **Agregar un Autor** → desde el navbar `Autores` o el botón del home  
   `http://127.0.0.1:8000/autores/agregar/`

2. **Agregar un Libro** → requiere tener al menos un autor cargado  
   `http://127.0.0.1:8000/libros/agregar/`

3. **Registrar un Préstamo** → requiere tener al menos un libro cargado  
   `http://127.0.0.1:8000/prestamos/registrar/`

4. **Buscar un libro** → por título o nombre de autor  
   `http://127.0.0.1:8000/libros/buscar/`

5. **Dashboard (home)** → muestra el resumen de libros disponibles y préstamos activos  
   `http://127.0.0.1:8000`

---

## Estructura del proyecto

```
web-python-django/
  Biblioteca/        → configuración del proyecto (settings, urls)
  catalogo/          → app principal
    models.py        → modelos: Autor, Libro, Prestamo
    views.py         → vistas de cada sección
    forms.py         → formularios para insertar y buscar datos
    urls.py          → rutas de la app
    templates/
      base.html               → template base (herencia)
      catalogo/
        index.html            → home / dashboard
        autores_lista.html    → lista de autores
        autor_form.html       → formulario agregar autor
        autor_detalle.html    → detalle del autor
        libros_lista.html     → lista de libros
        libro_form.html       → formulario agregar libro
        libro_detalle.html    → detalle del libro
        prestamos_lista.html  → lista de préstamos
        prestamo_form.html    → formulario registrar préstamo
        buscar.html           → buscador de libros
```

---

## Modelos

- **Autor** — nombre, país, año de nacimiento
- **Libro** — título, ISBN, año de publicación, cantidad disponible, FK a Autor
- **Prestamo** — fecha de préstamo, fecha de devolución, FK a Libro, nombre del usuario
