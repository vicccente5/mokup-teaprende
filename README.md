# TeaAprende — Proyecto Django (Evaluación 1, Programación Back End)

Plataforma educativa sobre el Trastorno del Espectro Autista (TEA), construida con Django.

## Requisitos

- Python 3.10+
- pip

## Instalación y ejecución

```bash
# 1. Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 2. Instalar Django
pip install django

# 3. Aplicar migraciones (crea la base de datos y carga los módulos/lecciones de ejemplo)
python manage.py migrate

# 4. Ejecutar el servidor de desarrollo
python manage.py runserver
```

Luego abre el navegador en **http://127.0.0.1:8000/**

## Flujo de uso

1. **`/` — Login:** ingresa cualquier nombre (no hay validación contra base de datos de usuarios, es solo demostrativo).
2. **`/dashboard/` — Panel principal:** muestra la ruta de aprendizaje con 5 módulos. El primero está desbloqueado; los demás se desbloquean al completar el anterior.
3. **`/leccion/<id>/` — Lección:** responde "Mito o Verdad" y recibe retroalimentación inmediata.

## Panel de administración

Para crear un usuario administrador y gestionar módulos/lecciones desde `/admin/`:

```bash
python manage.py createsuperuser
```

## Estructura del proyecto

```
teaaprende_django/
├── manage.py
├── db.sqlite3
├── teaaprende/            # Configuración del proyecto (settings, urls)
├── cursos/                # App principal: models, views, forms, admin
│   └── migrations/        # Incluye la carga automática de datos iniciales
├── templates/             # login.html, dashboard.html, leccion.html
└── static/                # css/styles.css, assets/mascot.jpg (del mockup original)
```

## Objetivo de Desarrollo Sostenible (ODS)

- **ODS 4 — Educación de calidad**
- **ODS 10 — Reducción de las desigualdades**

Ver `Informe_TeaAprende.docx` para el detalle completo del problema, la solución y las funcionalidades.
