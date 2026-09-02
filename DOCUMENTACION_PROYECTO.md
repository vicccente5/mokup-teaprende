# Documentación del Proyecto: TeaAprende

Este documento explica en detalle cómo está estructurado y cómo funciona el proyecto "TeaAprende", una plataforma web de aprendizaje interactiva construida con **Django** (Python). 

## Arquitectura General de Django (MVT)

Django utiliza un patrón de diseño llamado **MVT** (Modelo-Vista-Plantilla/Template). 

1. **Modelos (`models.py`)**: Se encargan de la base de datos. Definen la estructura de los datos (tablas).
2. **Vistas (`views.py`)**: Contienen la lógica principal ("el cerebro"). Reciben las peticiones del usuario, interactúan con los modelos para conseguir datos, y le dicen a las plantillas qué mostrar.
3. **Plantillas (`templates/`)**: Son los archivos HTML que muestran el resultado final al usuario en su navegador.
4. **Rutas (`urls.py`)**: Es el mapa del sitio web. Conecta una dirección web (ej: `/dashboard`) con la Vista que debe manejarla.

---

## Detalle de cada archivo y su función

### 1. `manage.py`
Este es el archivo principal de comandos de Django. Sirve como punto de entrada para ejecutar tareas administrativas. Cuando escribimos comandos en la terminal como `python manage.py runserver` (para iniciar la web) o `python manage.py migrate` (para actualizar la base de datos), este es el archivo que se está ejecutando. Lee la configuración del proyecto y lanza la instrucción correspondiente.

### 2. `teaaprende/urls.py`
Funciona como el **mapa de rutas** (enrutador) del proyecto principal. Contiene una lista llamada `urlpatterns` que asocia URLs específicas con sus respectivas vistas (funciones).
- `path('', login_view, ...)`: La ruta raíz (la página de inicio vacía) carga la vista de inicio de sesión.
- `path('dashboard/', dashboard_view, ...)`: La ruta del panel principal.
- `path('leccion/<int:leccion_id>/', leccion_view, ...)`: Una ruta dinámica que atrapa el número de la lección que el usuario quiere ver y se lo pasa a la vista correspondiente.

### 3. `cursos/models.py`
Aquí definimos nuestras tablas de base de datos como clases de Python.
- **`Modulo`**: Representa un tema principal (ej. "Introducción al TEA"). Tiene un título, descripción, orden e ícono.
- **`Leccion`**: Representa una actividad dentro del módulo, específicamente de tipo "Mito o Verdad". Está vinculada a un módulo a través de una **Llave Foránea** (`ForeignKey`), creando una relación en la que un módulo puede tener muchas lecciones. Guarda la pregunta, la respuesta correcta (`es_verdad`), la explicación de la respuesta y si ya fue `completada` por el usuario.

### 4. `cursos/views.py`
Es el corazón lógico de la aplicación. Contiene las funciones que procesan lo que el usuario pide:
- **`login_view`**: Se encarga de mostrar la pantalla de inicio y procesar el nombre del usuario. Como es una evaluación sin base de datos de usuarios real, simplemente toma el nombre escrito en el formulario y lo guarda en las variables de sesión del navegador (`request.session`).
- **`dashboard_view`**: 
  - Obtiene el nombre del usuario de la sesión.
  - Pide todos los `Modulo`s a la base de datos.
  - Calcula matemáticamente el progreso recorriendo cuántas lecciones totales tiene cada módulo y cuántas de ellas están `completada == True`.
  - Desbloquea módulos consecutivamente (un módulo solo se habilita si el anterior llegó al 100%).
  - Calcula el `progreso_general` y asigna un "Nivel" (Principiante, Intermedio, etc.) basado en el porcentaje global.
  - Finalmente, envía todos estos cálculos a la plantilla `dashboard.html` para ser dibujados.
- **`leccion_view`**: Recibe el identificador numérico (`leccion_id`) de la URL, busca la lección específica y compara la respuesta del usuario con la respuesta correcta registrada en la base de datos (`es_verdad`). Si coincide, cambia el estado de la lección a completada y la guarda.

### 5. `cursos/forms.py`
Define clases que generan formularios HTML de forma automática y ayudan a validar la información que ingresa el usuario.
- **`LoginForm`**: Crea los campos de "Usuario" y "Contraseña". Utiliza _widgets_ (componentes HTML) para poner estilos (clases CSS) y _placeholders_.
- **`RespuestaForm`**: Genera los botones de radio (bolitas de selección múltiple) para que el usuario elija exclusivamente entre "Mito" o "Verdad" en las lecciones.

### 6. `templates/` (Carpeta de Plantillas)
- **`login.html`**: Interfaz de ingreso a la plataforma.
- **`dashboard.html`**: Panel principal donde se ve la ruta de aprendizaje (módulos), barras de progreso interactivas y botones para acceder a las lecciones.
- **`leccion.html`**: Pantalla donde el usuario juega "Mito o Verdad". Muestra el formulario, la pregunta y el resultado de su respuesta (éxito o fallo) junto con la explicación.

---

## Flujo de Trabajo (¿Qué pasa cuando el usuario navega?)

1. **Ingreso a la web**: El usuario entra a `localhost:8000/`. El archivo `urls.py` detecta esta ruta y llama a `login_view()`. La vista dibuja `login.html`.
2. **Inicio de sesión**: El usuario escribe su nombre. `views.py` lo recibe usando `LoginForm`, lo valida, lo guarda en la sesión (`request.session`) y lo redirecciona a `/dashboard`.
3. **Panel Principal**: El `urls.py` detecta `/dashboard/` y llama a `dashboard_view()`. Esta vista hace consultas a la base de datos usando `models.py`, ejecuta matemáticas para ver el porcentaje completado y dibuja la interfaz con `dashboard.html`.
4. **Lección**: Al hacer clic en un botón "Comenzar", el usuario va a `/leccion/1/`. `urls.py` captura el "1" y llama a `leccion_view(request, 1)`. La vista carga la lección de la base de datos, muestra `leccion.html` con la ayuda de `RespuestaForm` y procesa si el usuario contestó bien para actualizar el porcentaje de avance.
