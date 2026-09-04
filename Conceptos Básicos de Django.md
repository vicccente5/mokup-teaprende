Conceptos Básicos de Django (Guía Rápida)
Django funciona con una arquitectura llamada MVT (Model-View-Template). Para que un usuario vea una página, haga clic en un botón y se guarde un dato, estos archivos trabajan en equipo.

Aquí tienes la explicación básica y "en humano" de qué hace cada parte:

1) Models (models.py) 🗄️
¿Qué es? Es el esqueleto de tu base de datos. ¿Qué hace? En lugar de escribir código complejo de bases de datos (SQL), en models.py creas Clases de Python. Django toma estas clases y las convierte automáticamente en tablas en la base de datos real.

Ejemplo en tu proyecto: Tienes el modelo Modulo y Leccion. Cada uno es una tabla. Si a Modulo le pones titulo = models.CharField(...), Django sabe que esa tabla necesita una columna de texto para el título.
Palabra clave para el profe: "Uso el ORM de Django para mapear objetos de Python a tablas de la base de datos".

Para entender cómo se conecta models.py con el motor principal de Django y con la base de datos, tienes que fijarte en tres piezas clave que trabajan juntas en tu proyecto:

1. El archivo settings.py (El enchufe principal)
En tu archivo teaaprende/settings.py hay dos configuraciones vitales que hacen que la conexión exista:

DATABASES: Hay un diccionario (casi al final del archivo) que le dice a Django a qué base de datos debe conectarse. En tu caso, está configurado para usar sqlite3 y le indica que guarde todo en un archivo llamado db.sqlite3.
INSTALLED_APPS: Al principio de settings.py agregaste tu aplicación 'cursos'. Sin esto, Django jamás leería tu archivo models.py. Al ponerla ahí, Django dice: "Ah, existe una app llamada cursos, voy a ir a buscar su archivo models.py para ver qué tablas necesita".
2. El ORM de Django (El Traductor)
Fíjate que al inicio de tu archivo models.py dice: from django.db import models. Esto es importar el ORM (Object-Relational Mapping). Es una herramienta interna de Django que sabe hablar "Python" y sabe hablar "SQL" (el lenguaje de las bases de datos). Cuando tú escribes models.CharField(), el ORM lo lee y lo traduce internamente a código SQL para enviárselo a la base de datos.

3. Las Migraciones (El puente de construcción)
Incluso si escribes tus modelos y configuras settings.py, la base de datos no se entera mágicamente de los cambios. Para conectarlos finalmente en la práctica, usas los comandos de la terminal:

python manage.py makemigrations: Django lee tu models.py y crea un "plano de construcción" de lo que cambiaste.
python manage.py migrate: Django toma ese plano, se conecta a db.sqlite3 a través de settings.py y construye las tablas reales usando el traductor (ORM).
En resumen (para el profe): "Los modelos se conectan a Django y a la base de datos a través de la configuración en settings.py, donde se define el motor (SQLite) y se registra la aplicación. Luego, el ORM de Django traduce nuestras clases de Python a tablas reales cuando ejecutamos las migraciones."


2) Views (views.py) 🧠
¿Qué es? Es el cerebro o el "controlador" de tu aplicación. ¿Qué hace? Es el intermediario. Cuando un usuario entra a una URL (como /dashboard/), la vista se encarga de:

Ir al Model a pedir los datos necesarios (ej. Tráeme todos los módulos completados).
Hacer cálculos o lógicas (ej. Calcular el porcentaje de progreso de este usuario).
Agarrar esos datos y enviárselos al Template para que se dibujen en la pantalla.
Ejemplo en tu proyecto: La función dashboard_view verifica si estás logueado, hace el cálculo matemático de tu progreso, y le manda esos números a dashboard.html.
3) Templates (Archivos .html) 🎨
¿Qué es? Es la cara visible de tu aplicación. ¿Qué hace? Son archivos HTML puros, pero con "poderes". Gracias a Django, puedes inyectar variables de Python directamente en el HTML usando llaves {{ }} o hacer bucles con {% %}.

Ejemplo en tu proyecto: En lugar de hacer 10 páginas distintas para 10 lecciones, haces un solo leccion.html y le dices: <h1>{{ leccion.pregunta }}</h1>. La vista se encargará de rellenar ese hueco con la pregunta correspondiente.
Palabra clave para el profe: "Utilizo el Motor de Plantillas de Django (Template Engine) para generar HTML dinámico".
4) Forms (forms.py) 🛡️
¿Qué es? Es la barrera de seguridad y el generador de formularios. ¿Qué hace? Tiene dos trabajos principales:

Dibujar: Genera automáticamente las cajas de texto (inputs) para el HTML para que no tengas que escribirlas a mano.
Validar (Lo más importante): Actúa como un guardia de seguridad. Revisa que los datos que envía el usuario sean correctos antes de que lleguen a la vista o a la base de datos.
Ejemplo en tu proyecto: Tu RegistroForm revisa que el correo ingresado termine en .com o .cl usando la función clean_email. Si el usuario pone un correo falso, el Formulario lo rechaza de inmediato.
En Resumen (El Viaje de un Dato)
El usuario entra a una URL y ve un Template con un Formulario.
Escribe sus datos y le da a "Enviar".
El Form revisa que los datos no sean falsos o maliciosos.
Si están bien, los datos pasan a la View.
La View procesa los datos y le dice al Model que los guarde en la base de datos.

