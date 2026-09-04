from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Modulo, Leccion

# Vista encargada de manejar el inicio de sesión.
# Verifica si las credenciales coinciden con algún usuario en la base de datos.
# Si los datos son correctos, inicia la sesión segura de Django y redirige al dashboard.
def login_view(request):
    """Vista de acceso a la plataforma con auth real."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    form = forms.LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['usuario']
        password = form.cleaned_data['contrasena']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Usuario o contraseña incorrectos.")

    return render(request, 'login.html', {'form': form})

# Vista para el registro de nuevos usuarios.
# Recibe los datos del formulario (usuario y contraseña validada), crea un nuevo
# registro en la base de datos y automáticamente inicia sesión con ese usuario.
def register_view(request):
    """Vista de registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    form = forms.RegistroForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
        
    return render(request, 'register.html', {'form': form})

# Vista simple para cerrar la sesión del usuario actual.
# Destruye la sesión de forma segura y lo devuelve a la pantalla de login.
def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('login')

# Vista principal (Dashboard), requiere que el usuario haya iniciado sesión (@login_required).
# Calcula el progreso individual de cada módulo y el progreso general sumando las lecciones
# completadas por el usuario, y determina su nivel (Principiante, Intermedio, etc.).
@login_required(login_url='login')
def dashboard_view(request):
    """Panel principal con la ruta de aprendizaje y cálculo de progreso."""
    usuario = request.user.username
    modulos = Modulo.objects.prefetch_related('lecciones').all()

    modulos_completados = 0
    modulo_anterior_completo = True

    for modulo in modulos:
        lecciones = modulo.lecciones.all()
        total_lecciones = len(lecciones)
        lecciones_completadas = sum(1 for leccion in lecciones if leccion.completada)

        modulo.progreso = int((lecciones_completadas / total_lecciones) * 100) if total_lecciones > 0 else 0
        modulo.esta_completo = (total_lecciones > 0 and lecciones_completadas == total_lecciones)
        modulo.desbloqueado = modulo_anterior_completo
        
        modulo_anterior_completo = modulo.esta_completo
        if modulo.esta_completo:
            modulos_completados += 1

    total_modulos = len(modulos)
    progreso_general = int((modulos_completados / total_modulos) * 100) if total_modulos > 0 else 0

    if progreso_general >= 76: nivel = 'Experto'
    elif progreso_general >= 51: nivel = 'Avanzado'
    elif progreso_general >= 26: nivel = 'Intermedio'
    else: nivel = 'Principiante'

    data = {
        'usuario': usuario,
        'modulos': modulos,
        'progreso_general': progreso_general,
        'nivel': nivel,
    }
    return render(request, 'dashboard.html', data)

# Vista de una lección específica, requiere que el usuario haya iniciado sesión.
# Muestra la pregunta (mito o verdad) y procesa la respuesta enviada por el formulario,
# marcando la lección como completada si el usuario acierta.
@login_required(login_url='login')
def leccion_view(request, leccion_id):
    """Muestra una lección y procesa la respuesta del usuario."""
    leccion = get_object_or_404(Leccion, id=leccion_id)
    form = forms.RespuestaForm(request.POST or None)
    resultado = None

    if request.method == 'POST' and form.is_valid():
        respuesta_es_verdad = (form.cleaned_data['respuesta'] == 'verdad')
        if respuesta_es_verdad == leccion.es_verdad:
            resultado = 'correcto'
            leccion.completada = True
            leccion.save()
        else:
            resultado = 'incorrecto'

    return render(request, 'leccion.html', {
        'leccion': leccion,
        'form': form,
        'resultado': resultado
    })

