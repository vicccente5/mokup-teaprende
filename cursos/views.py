from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Modulo, Leccion

# vista para el login
def login_view(request):
    # si ya inicio sesion lo mandamos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = forms.LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['contrasena']
        # Usamos email como username ya que así lo guardamos en el registro
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Correo o contraseña incorrectos.")
    return render(request, 'login.html', {'form': form})

# vista para registrarse
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')    
    form = forms.RegistroForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user) # iniciamos sesion al tiro
        return redirect('dashboard')
        
    return render(request, 'register.html', {'form': form})

# vista para salir
def logout_view(request):
    logout(request)
    return redirect('login')

# aca va el dashboard, solo entra si estas logueado
@login_required(login_url='login')
def dashboard_view(request):
    usuario = request.user.username
    modulos = Modulo.objects.prefetch_related('lecciones').all()
    modulos_completados = 0
    modulo_anterior_completo = True

    # sacar el porcentaje de progreso de cada modulo
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

    # ver en que nivel va
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

# vista para responder cada pregunta
@login_required(login_url='login')
def leccion_view(request, leccion_id):
    leccion = get_object_or_404(Leccion, id=leccion_id)
    form = forms.RespuestaForm(request.POST or None)
    resultado = None

    if request.method == 'POST' and form.is_valid():
        respuesta_es_verdad = (form.cleaned_data['respuesta'] == 'verdad')
        # ver si le achunto
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

