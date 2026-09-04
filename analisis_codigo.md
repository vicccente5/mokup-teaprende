# Análisis de Código de la Aplicación 'cursos'

A continuación se presenta un análisis detallado, línea por línea, de lo que hace el código en los archivos `models.py`, `forms.py` y `views.py` de la aplicación `cursos`.

---

## Análisis de `models.py`
Este archivo define la estructura de la base de datos (las tablas) utilizando el ORM (Object-Relational Mapping) de Django. Cada clase aquí representa una tabla en la base de datos y cada atributo es una columna.

```python
from django.db import models
```
- Importa el módulo `models` de Django. Este módulo contiene todas las herramientas necesarias para crear modelos de base de datos (clases de campos como `CharField`, relaciones como `ForeignKey`, etc.).

```python
# este es el modelo para los modulos del curso (como los temas)
class Modulo(models.Model):
```
- Un comentario explicando el propósito del modelo.
- Declara la clase `Modulo` que hereda de `models.Model`. Al heredar de `models.Model`, Django sabe que esto debe convertirse en una tabla de la base de datos (probablemente llamada `cursos_modulo`).

```python
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField() # aca guardamos el orden 1, 2, 3...
    icono = models.CharField(max_length=50, default='fa-solid fa-puzzle-piece')
```
- `titulo`: Crea una columna de tipo texto corto (`CharField`) con un límite máximo de 200 caracteres.
- `descripcion`: Crea una columna de tipo texto largo (`TextField`), ideal para párrafos extensos ya que no tiene un límite fijo estricto como `CharField`.
- `orden`: Crea una columna que almacena un número entero positivo (`PositiveIntegerField`). Se usará para saber en qué posición va cada módulo (1, 2, 3...).
- `icono`: Crea una columna que almacena una cadena de texto corta (máximo 50 caracteres) con un valor por defecto `'fa-solid fa-puzzle-piece'` (parece ser una clase de icono de FontAwesome).

```python
    class Meta:
        ordering = ['orden']
```
- La subclase `Meta` proporciona metadatos al modelo. Aquí, `ordering = ['orden']` le dice a Django que cada vez que se consulten los módulos desde la base de datos, por defecto vengan ordenados ascendentemente según su campo `orden`.

```python
    def __str__(self):
        return f"Módulo {self.orden}: {self.titulo}"
```
- Define el método `__str__`, que indica cómo se debe representar un objeto `Modulo` cuando se convierte a texto (por ejemplo, en el panel de administración de Django). Devolverá algo como `"Módulo 1: Introducción"`.

```python
# esta tabla es para cada pregunta de verdadero o falso que va dentro del modulo
class Leccion(models.Model):
```
- Comentario y declaración de la clase `Leccion`, que será otra tabla en la base de datos, usada para representar preguntas/lecciones individuales de tipo "Mito o Verdad".

```python
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
```
- Crea una columna relacional (clave foránea). Esto vincula cada "Lección" a un "Módulo" específico (relación de muchos a uno). 
  - `on_delete=models.CASCADE` significa que si se elimina el Módulo, todas las Lecciones asociadas a él también se borrarán.
  - `related_name='lecciones'` crea un "atajo" inverso. Si tienes un objeto Módulo, puedes acceder a todas sus lecciones usando `modulo.lecciones.all()`.

```python
    pregunta = models.CharField(max_length=300)
    es_verdad = models.BooleanField() # true si es verdad, false si es un mito
    explicacion = models.TextField()
    completada = models.BooleanField(default=False)
```
- `pregunta`: Columna de tipo texto corto, hasta 300 caracteres.
- `es_verdad`: Columna de tipo booleano (True o False). Representa si la afirmación es cierta o es un mito.
- `explicacion`: Columna de texto largo que guardará la retroalimentación o justificación.
- `completada`: Columna de tipo booleano con valor inicial `False`. Esto rastrea si el usuario ya ha superado esta lección. *(Ojo con este diseño: este campo es global para la lección; si varios usuarios usan la app, todos compartirían el estado `completada` de la lección, lo cual podría ser un bug si se esperan múltiples usuarios).*

```python
    def __str__(self):
        return self.pregunta
```
- Define cómo se muestra la lección como texto, retornando simplemente el texto de la pregunta.

---

## Análisis de `forms.py`
Aquí se manejan los formularios de la aplicación. Django facilita la creación de formularios HTML y la validación de los datos enviados (POST).

```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
```
- Importa el módulo de formularios base de Django.
- Importa el modelo `User` integrado en Django, que gestiona a los usuarios registrados.
- Importa `UserCreationForm`, un formulario prefabricado de Django para registrar nuevos usuarios con contraseña.

```python
# form para iniciar sesion
class LoginForm(forms.Form):
```
- Define `LoginForm`, que hereda de `forms.Form` (formulario básico sin atadura directa a un modelo de BD).

```python
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
```
- Define un campo `email`. `forms.EmailField` valida automáticamente que lo introducido tenga formato de correo (@).
  - `label="Correo"` es el texto que acompañará al campo.
  - `widget=forms.EmailInput(...)` configura cómo se renderizará el HTML. Le añade la clase CSS `form-input` y un texto `placeholder`.

```python
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'})
    )
```
- Define el campo `contrasena`. Usa un `PasswordInput` para que los caracteres se oculten al escribir. También le añade clases CSS y un placeholder.

```python
# form para el registro de los profes o papas (solo pide correo y pass)
class RegistroForm(UserCreationForm):
```
- Define `RegistroForm`, que hereda de `UserCreationForm`. Heredar de aquí le da gratis los campos de contraseña y confirmación de contraseña, además de la lógica de validarlas y hashearlas.

```python
    username = None # ocultamos el username porque usaremos el correo
```
- Elimina el campo "username" que viene por defecto en el `UserCreationForm` porque esta aplicación quiere registrar usando solo el correo.

```python
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
```
- Añade explícitamente un campo de email al formulario de registro con sus clases y placeholders.

```python
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",) # la pass la pone django automatico
```
- La clase `Meta` configura el formulario de modelo. Indica que el modelo asociado es `User` y que el único campo a mostrar (además de los de contraseñas que `UserCreationForm` inyecta automáticamente) es `"email"`.

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # aca le pongo la clase de css a todos los inputs para que se vean bien
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
```
- Sobrescribe el constructor (`__init__`) del formulario. Primero llama al constructor original (`super()`). Luego, itera por todos los campos generados y les inyecta el atributo HTML `class="form-input"`. Esto asegura que incluso los campos de contraseña generados automáticamente tengan el estilo correcto.

```python
    def clean_email(self):
        # validar que el correo termine en algo valido
        email = self.cleaned_data.get('email')
```
- El método `clean_email` es un "hook" de validación personalizada de Django. Se ejecuta automáticamente para validar el campo `email`. Extrae el valor del correo.

```python
        if email:
            dominios = (".com", ".cl", ".net", ".org", ".edu")
            if not email.endswith(dominios):
                raise forms.ValidationError("Usa un correo valido por favor (.com, .cl)")
```
- Si se ingresó un correo, verifica que termine en una tupla de dominios permitidos usando `endswith()`. Si no coincide, levanta un `ValidationError` que detendrá el envío del formulario y mostrará ese mensaje de error al usuario.

```python
        # revisar si ya existe alguien con este correo
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
            
        return email
```
- Hace una consulta a la base de datos comprobando si ya existe un usuario con ese mismo email. Si existe, arroja otro error. Finalmente, retorna el correo limpio.

```python
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email # guardamos el correo en el username para que django no reclame
        if commit:
            user.save()
        return user
```
- Sobrescribe el método `save()`. `commit=False` crea la instancia del usuario pero no la guarda en la base de datos todavía. Luego copia el `email` y lo pega en el atributo `username` (porque Django internamente requiere un `username` obligatorio en su modelo `User`). Finalmente, lo guarda en la base de datos (`user.save()`) y lo retorna.

```python
# form para responder las lecciones
class RespuestaForm(forms.Form):
    OPCIONES = [
        ('verdad', 'Verdad'),
        ('mito', 'Mito'),
    ]
    respuesta = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.RadioSelect,
        label="¿Mito o Verdad?"
    )
```
- Crea un formulario muy simple `RespuestaForm` con un solo campo de opciones (`ChoiceField`).
  - Las opciones son una lista de tuplas: `('verdad', 'Verdad')` donde el primer valor es lo que viaja al backend y el segundo es lo que lee el usuario en pantalla.
  - `widget=forms.RadioSelect` renderiza las opciones como "botones de radio" (círculos seleccionables) en lugar de una lista desplegable.

---

## Análisis de `views.py`
Las vistas actúan como controladores: reciben las peticiones web (requests), procesan datos (leyendo modelos o validando formularios) y devuelven una respuesta (generalmente un archivo HTML renderizado o una redirección).

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Modulo, Leccion
```
- Importa utilidades. `render` devuelve HTML, `redirect` manda al usuario a otra URL, y `get_object_or_404` busca un elemento en BD o muestra un error 404 si no existe.
- Importa funciones del sistema de autenticación de Django y el decorador `login_required` para proteger rutas.
- Importa los formularios y modelos que analizamos antes.

```python
# vista para el login
def login_view(request):
    # si ya inicio sesion lo mandamos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
```
- Define la vista de inicio de sesión. Si el usuario que accede a esta página ya tiene una sesión iniciada activa (`request.user.is_authenticated`), lo redirige automáticamente a la página llamada 'dashboard' (para que no vea la pantalla de login inútilmente).

```python
    form = forms.LoginForm(request.POST or None)
```
- Instancia el formulario de login. `request.POST or None` significa: si la petición es POST, rellena el form con los datos enviados por el usuario. Si es GET, el form estará vacío.

```python
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['contrasena']
```
- Si la petición es un envío de datos (POST) y el formulario pasó las validaciones de formato, extrae el email y la contraseña limpios.

```python
        # Usamos email como username ya que así lo guardamos en el registro
        user = authenticate(request, username=email, password=password)
```
- Intenta autenticar al usuario usando `authenticate()`. Como en el registro (`forms.py`) guardamos el email dentro del campo `username`, aquí le pasamos el email en el argumento `username` para buscarlo en la BD. Si las credenciales son correctas, retorna el objeto del usuario; si no, retorna `None`.

```python
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Correo o contraseña incorrectos.")
```
- Si `user` se encontró (no es `None`), se crea la sesión en el navegador (`login(request, user)`) y redirige al dashboard. Si fue `None`, agrega un error general (`None` como primer argumento) al formulario diciendo que los datos son incorrectos.

```python
    return render(request, 'login.html', {'form': form})
```
- Renderiza la plantilla `login.html` y le pasa el `form` (ya sea vacío para un GET, o con los datos/errores para un POST fallido).

```python
# vista para registrarse
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')    
    form = forms.RegistroForm(request.POST or None)
```
- Similar al login, protege para no registrar estando logueado, e instancia `RegistroForm`.

```python
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user) # iniciamos sesion al tiro
        return redirect('dashboard')
```
- Si se envía el form por POST y es válido (pasa validación de dominios permitidos y existencia, definidos en el form), lo guarda (`form.save()`), lo cual invoca el método custom que vimos que setea el `username`. Tras crearlo, automáticamente inicia sesión y lo envía al dashboard.

```python
    return render(request, 'register.html', {'form': form})
```
- Renderiza el template HTML pasando el form de registro.

```python
# vista para salir
def logout_view(request):
    logout(request)
    return redirect('login')
```
- Vista de cerrar sesión. Borra las cookies de sesión del usuario con `logout()` y lo redirige a la página de login.

```python
# aca va el dashboard, solo entra si estas logueado
@login_required(login_url='login')
def dashboard_view(request):
```
- El decorador `@login_required` protege esta vista. Si un usuario anónimo intenta entrar a la URL del dashboard, Django intercepta la petición y lo redirige a la URL `'login'`.

```python
    usuario = request.user.username
    modulos = Modulo.objects.prefetch_related('lecciones').all()
```
- Toma el "username" del usuario logueado (que será su correo) para probablemente saludarlo en el HTML.
- Trae todos los módulos de la base de datos. Usa `prefetch_related('lecciones')`, lo cual es una **excelente optimización de base de datos**: con esto, Django trae todas las lecciones asociadas a esos módulos en una sola consulta extra, evitando el problema de "N+1 consultas" en el bucle que viene abajo.

```python
    modulos_completados = 0
    modulo_anterior_completo = True
```
- Inicializa variables de estado. `modulos_completados` será un contador, y `modulo_anterior_completo` se usa para saber si el módulo actual en el ciclo debería estar desbloqueado.

```python
    # sacar el porcentaje de progreso de cada modulo
    for modulo in modulos:
        lecciones = modulo.lecciones.all()
        total_lecciones = len(lecciones)
```
- Itera por cada módulo. Recupera la lista de lecciones y cuenta cuántas hay.

```python
        lecciones_completadas = sum(1 for leccion in lecciones if leccion.completada)
        modulo.progreso = int((lecciones_completadas / total_lecciones) * 100) if total_lecciones > 0 else 0
```
- Cuenta cuántas lecciones tienen `completada == True`.
- Calcula dinámicamente un atributo nuevo `.progreso` (porcentaje 0-100) y se lo inyecta al objeto `modulo`. Hace una validación de división segura (por si `total_lecciones` es 0).

```python
        modulo.esta_completo = (total_lecciones > 0 and lecciones_completadas == total_lecciones)
        modulo.desbloqueado = modulo_anterior_completo
        modulo_anterior_completo = modulo.esta_completo
```
- Determina si el módulo está completo (si la cantidad de completadas es igual al total).
- Determina si el usuario puede acceder al módulo. Se desbloquea si el **módulo anterior** estaba completo.
- Actualiza `modulo_anterior_completo` con el estado del módulo actual. Para la primera iteración, siempre está desbloqueado.

```python
        if modulo.esta_completo:
            modulos_completados += 1
```
- Incrementa el contador global de módulos completados.

```python
    total_modulos = len(modulos)
    progreso_general = int((modulos_completados / total_modulos) * 100) if total_modulos > 0 else 0
```
- Calcula el porcentaje de avance global de todos los módulos combinados.

```python
    # ver en que nivel va
    if progreso_general >= 76: nivel = 'Experto'
    elif progreso_general >= 51: nivel = 'Avanzado'
    elif progreso_general >= 26: nivel = 'Intermedio'
    else: nivel = 'Principiante'
```
- Asigna una categoría de "nivel" basada en el progreso global.

```python
    data = {
        'usuario': usuario,
        'modulos': modulos,
        'progreso_general': progreso_general,
        'nivel': nivel,
    }
    return render(request, 'dashboard.html', data)
```
- Empaqueta todas las variables calculadas en un diccionario `data` (contexto) y las pasa al HTML `dashboard.html` para ser mostradas en pantalla.

```python
# vista para responder cada pregunta
@login_required(login_url='login')
def leccion_view(request, leccion_id):
```
- Vista protegida para mostrar y responder una lección específica. Recibe un parámetro extra por URL: `leccion_id`.

```python
    leccion = get_object_or_404(Leccion, id=leccion_id)
    form = forms.RespuestaForm(request.POST or None)
    resultado = None
```
- Busca la lección en la BD. Si un usuario pone un ID que no existe (ej: URL/leccion/999), Django mostrará un error 404 (página no encontrada) en lugar de un colapso del sistema.
- Instancia el formulario de respuesta.
- Inicializa la variable `resultado` en vacía, para mostrar mensajes de acierto/error más tarde en el HTML.

```python
    if request.method == 'POST' and form.is_valid():
        respuesta_es_verdad = (form.cleaned_data['respuesta'] == 'verdad')
```
- Si se envió una respuesta, extrae si el usuario contestó "verdad" y lo transforma a un valor booleano (True o False).

```python
        # ver si le achunto
        if respuesta_es_verdad == leccion.es_verdad:
            resultado = 'correcto'
            leccion.completada = True
            leccion.save()
```
- Compara la respuesta convertida a booleano con el valor `es_verdad` de la base de datos de esa lección. Si coinciden, marca `resultado = 'correcto'`, setea `leccion.completada = True` y **guarda este cambio en la base de datos**.

```python
        else:
            resultado = 'incorrecto'
```
- Si no coinciden (ej. puso verdad pero era mito), establece que el resultado es `'incorrecto'` y no la guarda como completada.

```python
    return render(request, 'leccion.html', {
        'leccion': leccion,
        'form': form,
        'resultado': resultado
    })
```
- Renderiza `leccion.html`, entregándole la lección específica (con sus preguntas/explicaciones para mostrar), el formulario de botones de radio, y el estado de la respuesta (`None`, `'correcto'` o `'incorrecto'`) para mostrar mensajes de éxito o fallo.
