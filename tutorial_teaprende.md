# Tutorial Completo: Creando la Plataforma Educativa "TeaAprende" desde cero

Este tutorial te guiará paso a paso, sin saltarse ningún detalle, para construir la plataforma web "TeaAprende" utilizando el framework Django (Python). Se explicará línea por línea el código utilizado.

## Paso 1: Preparación del Entorno

1. Abre tu terminal (Símbolo del sistema o PowerShell).
2. Crea una carpeta para tu proyecto y entra en ella:
   ```bash
   mkdir mi_teaprende
   cd mi_teaprende
   ```
3. Crea un entorno virtual para aislar las librerías. Esto asegura que no interfieran con otros proyectos:
   ```bash
   python -m venv venv
   ```
4. Activa el entorno virtual:
   * En Windows: `.\venv\Scripts\activate`
   * En Mac/Linux: `source venv/bin/activate`
5. Instala el framework Django:
   ```bash
   pip install django
   ```

## Paso 2: Creación del Proyecto y la Aplicación

1. Crea el proyecto principal llamado `teaaprende`:
   ```bash
   django-admin startproject teaaprende .
   ```
   *(El punto al final es muy importante, le dice a Django que cree la configuración en la carpeta actual).*

2. Crea la aplicación (módulo) llamada `cursos` que manejará la lógica de las clases:
   ```bash
   python manage.py startapp cursos
   ```

## Paso 3: Configuración Principal (`settings.py`)

Abre el archivo `teaaprende/settings.py`. Este es el cerebro de configuración de tu proyecto.

### 1. Registrar la Aplicación
Busca la lista `INSTALLED_APPS` y agrega `'cursos'` al final. Esto le dice a Django que reconozca nuestra aplicación:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cursos', # Agregamos nuestra aplicación recién creada
]
```

### 2. Configurar las Plantillas (HTML)
Busca la lista `TEMPLATES`. En la clave `DIRS` agrega la ruta para la carpeta donde estarán nuestros diseños:

```python
import os # Asegúrate de importar os al inicio del archivo (o usa BASE_DIR que ya viene importado con pathlib)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Indicamos a Django dónde buscar los archivos HTML (en una carpeta llamada 'templates' en la raíz)
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': { ... },
    },
]
```

### 3. Configurar los Archivos Estáticos (CSS e Imágenes)
Ve al final de `settings.py` y agrega la ruta para que Django encuentre tus estilos:

```python
STATIC_URL = 'static/'
# Le decimos a Django en qué carpeta externa guardaremos el CSS
STATICFILES_DIRS = [BASE_DIR / 'static'] 
```

---

## Paso 4: Creación de los Modelos (`cursos/models.py`)

Los modelos definen la estructura de tu base de datos mediante programación orientada a objetos. Reemplaza el código en `cursos/models.py`:

```python
from django.db import models # Importa las herramientas base para crear tablas

class Modulo(models.Model):
    # Campo de texto corto (max_length indica que no puede superar 200 caracteres)
    titulo = models.CharField(max_length=200)
    # Campo de texto grande e ilimitado para una descripción
    descripcion = models.TextField()
    # Campo numérico positivo. help_text es un comentario para el administrador
    orden = models.PositiveIntegerField(help_text="Posición del módulo en la ruta")
    # Texto corto para guardar qué clase de icono usar (ej: FontAwesome)
    icono = models.CharField(max_length=50, default='fa-solid fa-puzzle-piece')

    class Meta:
        # Define que siempre que consultemos a los módulos, vengan ordenados por su campo 'orden'
        ordering = ['orden']

    def __str__(self):
        # Esta función mágica determina cómo se leerá el objeto en formato texto (ej: "Módulo 1: Introducción")
        return f"Módulo {self.orden}: {self.titulo}"


class Leccion(models.Model):
    # Clave foránea: Relaciona cada lección con un módulo. Si se borra el módulo, se borran sus lecciones (CASCADE).
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    # La afirmación que el usuario deberá catalogar
    pregunta = models.CharField(max_length=300)
    # Booleano: guarda 'True' si la pregunta es Verdad, o 'False' si es Mito.
    es_verdad = models.BooleanField()
    # La explicación que se le da al usuario tras contestar
    explicacion = models.TextField()
    # Casilla que indica si el usuario acertó la pregunta. Por defecto, cuando se crea, es False.
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.pregunta
```

---

## Paso 5: Creación de Formularios (`cursos/forms.py`)

Django genera el HTML de los formularios por nosotros para mayor seguridad. Crea el archivo `cursos/forms.py`:

```python
from django import forms # Importa el generador de formularios

class LoginForm(forms.Form):
    # Genera un <input type="email">. Asigna clases de CSS y un placeholder
    usuario = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
    # Genera un <input type="password"> (oculta los caracteres digitados)
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )

    def clean_contrasena(self):
        # clean_nombrecampo es una función especial que Django ejecuta para validar un dato específico
        contrasena = self.cleaned_data.get('contrasena')
        # Si existe contraseña pero es menor a 6 caracteres...
        if contrasena and len(contrasena) < 6:
            # Disparamos un error que el formulario le mostrará al usuario
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return contrasena


class RespuestaForm(forms.Form):
    # Lista con las opciones posibles. El primer valor es cómo se guarda, el segundo cómo se lee.
    OPCIONES = [
        ('verdad', 'Verdad'),
        ('mito', 'Mito'),
    ]
    # Genera un grupo de opciones obligando a elegir solo una.
    respuesta = forms.ChoiceField(
        choices=OPCIONES, 
        widget=forms.RadioSelect, # Lo dibuja en HTML como bolitas seleccionables y no como una lista desplegable
        label="¿Mito o Verdad?"
    )
```

---

## Paso 6: La Lógica, Las Vistas (`cursos/views.py`)

Las vistas son funciones que reciben la petición web (request) y deciden qué HTML y qué datos devolver. Copia esto en `cursos/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Modulo, Leccion

def login_view(request):
    form = forms.LoginForm() # Creamos el formulario vacío

    if request.method == 'POST': # Verifica si el usuario envió información haciendo click
        form = forms.LoginForm(request.POST) # Carga la información que el usuario envió al formulario
        if form.is_valid(): # Llama a las validaciones (como clean_contrasena)
            usuario = form.cleaned_data['usuario'] # Extrae el correo ya limpio y validado
            request.session['usuario'] = usuario # Guarda el correo en las "cookies/sesión" de la memoria del navegador
            return redirect('dashboard') # Envía al usuario de inmediato a la ruta llamada 'dashboard'

    # Dibuja la plantilla 'login.html', inyectándole la variable 'form'
    return render(request, 'login.html', {'form': form})


def dashboard_view(request):
    # Extrae el usuario de la memoria. Si nadie inició sesión, devuelve "Invitado"
    usuario = request.session.get('usuario', 'Invitado')
    modulos = Modulo.objects.all() # Consulta SQL que trae TODOS los módulos

    modulos_completados = 0
    modulo_anterior_completo = True # Arrancamos en True para que el primer módulo esté siempre desbloqueado

    for modulo in modulos: # Ciclo que recorre cada módulo uno por uno
        lecciones = modulo.lecciones.all() # Trae todas las lecciones asociadas a este módulo
        total = lecciones.count() # Cuenta cuántas lecciones tiene
        completadas = sum(1 for l in lecciones if l.completada) # Suma 1 por cada lección que tenga "completada=True"

        if total > 0:
            modulo.progreso = int((completadas / total) * 100) # Calcula el porcentaje matemático
        else:
            modulo.progreso = 0

        # Un módulo está listo solo si tiene lecciones y todas están completas
        modulo.esta_completo = (total > 0 and completadas == total)
        # Habilitamos el módulo actual solo si el módulo en la vuelta anterior del ciclo estaba completo
        modulo.desbloqueado = modulo_anterior_completo
        
        # Pisamos esta variable con el estado de nuestro módulo actual para que le sirva a la vuelta siguiente del ciclo
        modulo_anterior_completo = modulo.esta_completo

        if modulo.esta_completo:
            modulos_completados += 1 # Aumenta la cantidad de módulos listos

    total_modulos = modulos.count()
    # Regla de tres simple para el progreso general global
    progreso_general = int((modulos_completados / total_modulos) * 100) if total_modulos > 0 else 0

    # Lógica simple para gamificación y asignar nivel
    nivel = "Principiante"
    if progreso_general == 100: nivel = "Experto"
    elif progreso_general >= 50: nivel = "Intermedio"

    # Empaquetamos toda la matemática y los resultados en un diccionario "data"
    data = {
        'usuario': usuario,
        'modulos': modulos,
        'progreso_general': progreso_general,
        'nivel': nivel
    }
    # Dibuja dashboard.html con la data calculada
    return render(request, 'dashboard.html', data)


def leccion_view(request, leccion_id):
    # Busca la lección según su ID o lanza el error "Página 404 no encontrada" si el ID no existe
    leccion = get_object_or_404(Leccion, id=leccion_id)
    form = forms.RespuestaForm()
    resultado = None # Empezamos sin evaluar al usuario

    if request.method == 'POST':
        form = forms.RespuestaForm(request.POST)
        if form.is_valid():
            # Extrae la palabra enviada (verdad o mito)
            respuesta_usuario = form.cleaned_data['respuesta']
            # Creamos una variable booleana True si eligió 'verdad', False si eligió 'mito'
            es_verdad_usuario = (respuesta_usuario == 'verdad')

            # Si lo que ingresó el usuario concuerda con lo registrado en la base de datos de esa lección
            if es_verdad_usuario == leccion.es_verdad:
                resultado = 'correcto'
                leccion.completada = True # Cambia el estado
                leccion.save() # Guarda obligatoriamente en base de datos para no perderlo
            else:
                resultado = 'incorrecto'

    data = {
        'leccion': leccion,
        'form': form,
        'resultado': resultado
    }
    return render(request, 'leccion.html', data)
```

---

## Paso 7: Enrutador de URLs (`teaaprende/urls.py`)

Abre el archivo `teaaprende/urls.py`. Este archivo vincula una dirección de internet (URL) con las Vistas que acabas de crear:

```python
from django.contrib import admin
from django.urls import path
from cursos.views import login_view, dashboard_view, leccion_view # Importamos todas las vistas

urlpatterns = [
    path('admin/', admin.site.urls), # Ruta obligatoria para el panel de administración
    
    # Ruta vacía ('') equivale a la página de inicio. Apunta a login_view.
    path('', login_view, name='login'), 
    
    # Ruta /dashboard/ apunta a dashboard_view
    path('dashboard/', dashboard_view, name='dashboard'), 
    
    # <int:leccion_id> es una variable dinámica. Captura el número en la URL (ej: leccion/2/) y se lo manda a leccion_view
    path('leccion/<int:leccion_id>/', leccion_view, name='leccion'), 
]
```

---

## Paso 8: Creación de Plantillas (HTML)

Crea una carpeta llamada `templates` en la raíz de tu proyecto. Adentro, crea `login.html`:

**`templates/login.html`**
```html
<!-- Carga el motor de estáticos para poder referenciar CSS e imágenes -->
{% load static %} 
<!DOCTYPE html>
<html lang="es">
<head>
    <title>TeaAprende - Iniciar Sesión</title>
    <!-- Vincula el archivo CSS dinámicamente sin importar dónde esté tu servidor alojado -->
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    <!-- tag 'form' con método 'POST' para seguridad -->
    <form method="POST">
        <!-- El CSRF Token es OBLIGATORIO en Django, previene ataques falsificando tu identidad (Cross Site Request Forgery) -->
        {% csrf_token %} 
        
        <!-- Dibuja los componentes del formulario que creamos en forms.py -->
        {{ form.usuario }}
        {{ form.contrasena }}
        
        <button type="submit">Ingresar</button>
    </form>
</body>
</html>
```

*Para las otras dos pantallas, debes crear `dashboard.html` y `leccion.html` e insertar tu diseño completo. Los datos calculados en las vistas los imprimes usando `{{ variable }}` y las lógicas en HTML se escriben como `{% for modulo en modulos %}` y `{% if resultado == 'correcto' %}`.*

---

## Paso 9: Base de Datos y Ejecución Final

Llegó la hora de encender todo:

1. Crea las instrucciones SQL para estructurar la base de datos:
   ```bash
   python manage.py makemigrations
   ```
2. Ejecuta y materializa las instrucciones para crear las tablas reales:
   ```bash
   python manage.py migrate
   ```
3. Finalmente, enciende el servidor de pruebas local:
   ```bash
   python manage.py runserver
   ```

Ve a tu navegador e ingresa a `http://127.0.0.1:8000/`. ¡Listo, has construido **TeaAprende** desde cero!
