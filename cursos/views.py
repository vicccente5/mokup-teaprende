from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Modulo, Leccion


def login_view(request):
    """
    Vista de acceso a la plataforma.
    No usa un sistema de usuarios real (fuera del alcance de esta evaluación):
    solo guarda el nombre ingresado en la sesión para personalizar el dashboard.
    """
    form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            request.session['usuario'] = usuario
            return redirect('dashboard')

    data = {'form': form}
    return render(request, 'login.html', data)


def dashboard_view(request):
    """
    Panel principal: muestra la ruta de aprendizaje (lista de módulos)
    y calcula el progreso general del usuario recorriendo sus lecciones.
    """
    usuario = request.session.get('usuario', 'Invitado')
    modulos = Modulo.objects.all()

    modulos_completados = 0
    modulo_anterior_completo = True  # el primer módulo siempre parte desbloqueado

    # Recorremos cada módulo (ciclo for) para calcular su progreso individual
    for modulo in modulos:
        lecciones = modulo.lecciones.all()
        total_lecciones = lecciones.count()
        lecciones_completadas = 0

        for leccion in lecciones:
            if leccion.completada:          # estructura condicional if
                lecciones_completadas += 1

        if total_lecciones > 0:
            modulo.progreso = int((lecciones_completadas / total_lecciones) * 100)
        else:
            modulo.progreso = 0

        modulo.esta_completo = (total_lecciones > 0 and lecciones_completadas == total_lecciones)

        # Un módulo se desbloquea solo si el anterior ya fue completado
        modulo.desbloqueado = modulo_anterior_completo
        modulo_anterior_completo = modulo.esta_completo

        if modulo.esta_completo:
            modulos_completados += 1

    total_modulos = modulos.count()
    if total_modulos > 0:
        progreso_general = int((modulos_completados / total_modulos) * 100)
    else:
        progreso_general = 0

    # Estructura condicional if / elif / else para determinar el nivel del usuario
    if progreso_general >= 76:
        nivel = 'Experto'
    elif progreso_general >= 51:
        nivel = 'Avanzado'
    elif progreso_general >= 26:
        nivel = 'Intermedio'
    else:
        nivel = 'Principiante'

    data = {
        'usuario': usuario,
        'modulos': modulos,
        'progreso_general': progreso_general,
        'nivel': nivel,
    }
    return render(request, 'dashboard.html', data)


def leccion_view(request, leccion_id):
    """
    Muestra una lección tipo "Mito o Verdad" y procesa la respuesta del usuario.
    Si la respuesta es correcta, marca la lección como completada.
    """
    leccion = get_object_or_404(Leccion, id=leccion_id)
    form = forms.RespuestaForm()
    resultado = None

    if request.method == 'POST':
        form = forms.RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.cleaned_data['respuesta']
            respuesta_es_verdad = (respuesta == 'verdad')

            if respuesta_es_verdad == leccion.es_verdad:
                resultado = 'correcto'
                leccion.completada = True
                leccion.save()
            else:
                resultado = 'incorrecto'

    data = {
        'leccion': leccion,
        'form': form,
        'resultado': resultado,
    }
    return render(request, 'leccion.html', data)
