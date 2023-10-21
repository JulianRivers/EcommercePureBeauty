# TravelEasy✈️

Sistema de gestión de viaticos hecho  en Django 4.1.2🐍

## Instalación y configuración⚙️

### 1. Clonar el proyecto

```bash
git clone https://github.com/JulianRivers/TravelEasy.git
cd TravelEasy
```

### 2. Instalar dependencias y configurar venv

Este comando es importante para instalar todo lo que usa el proyecto y este pueda ejecutarse correctamente

```bash
pip install -r .\requirements.txt
```

### 3. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py makemigrations gerente
python manage.py migrate
```

### 4. Ejecutar

#### Localhost

Solo debes correr este comando:

```bash
python manage.py runserver
```

Después de esto, podrás encontrar la aplicación corriendo en <http://127.0.0.1:8000/>

---

### Crear superusuarios

```bash
python manage.py createsuperuser
```

te pedirá Email, Nombres, Apellidos, Password

### Usuarios 👩‍💻🧑‍💻

Dejaré unos usuarios registrados

```usuario administrador/gerente```

- **correo**: <admin@admin.com>
- **contraseña**: 1234

```usuario empleado con eventos y viaticos```

- **correo**: <empleado@traveleasy.com>
- **contraseña**: 1234
