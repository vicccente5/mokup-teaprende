# Importaciones de funciones de Django necesarias para procesar las vistas
from django.shortcuts import render, redirect, get_object_or_404
# Importamos los formularios y modelos que usamos en esta aplicación
from . import forms
from .models import Modulo, Leccion


def login_view(request):
    """
    Vista de acceso a la plataforma.
    No usa un sistema de usuarios real (fuera del alcance de esta evaluación):
    solo guarda el nombre ingresado en la sesión para personalizar el dashboard.
    """
    # Creamos una instancia del formulario de Login vacío
    form = forms.LoginForm()

    # Comprobamos si el usuario ha enviado datos (método POST)
    if request.method == 'POST':
        # Instanciamos el formulario pasándole los datos enviados (request.POST)
        form = forms.LoginForm(request.POST)
        # Validamos que los datos ingresados en el formulario sean correctos
        if form.is_valid():
            # Extraemos el nombre de usuario de los datos limpios (validados)
            usuario = form.cleaned_data['usuario']
            # Guardamos el nombre del usuario en las variables de sesión del navegador
            request.session['usuario'] = usuario
            # Redirigimos al usuario a la vista nombrada 'dashboard'
            return redirect('dashboard')

    # Diccionario 'data' (contexto) que pasaremos a la plantilla HTML
    data = {'form': form}
    # Renderizamos (dibujamos) la plantilla 'login.html' pasándole los datos
    return render(request, 'login.html', data)


def dashboard_view(request):
    """
    Panel principal: muestra la ruta de aprendizaje (lista de módulos)
    y calcula el progreso general del usuario recorriendo sus lecciones.
    """
    # Obtenemos el usuario de la sesión, si no existe usamos 'Invitado'
    usuario = request.session.get('usuario', 'Invitado')
    
    # Traemos todos los registros del modelo Modulo desde la base de datos
    modulos = Modulo.objects.all()

    # Variables para calcular el progreso total
    modulos_completados = 0
    modulo_anterior_completo = True  # el primer módulo siempre parte desbloqueado

    # Recorremos cada módulo (ciclo for) para calcular su progreso individual
    for modulo in modulos:
        # Obtenemos todas las lecciones asociadas a este módulo en particular
        lecciones = modulo.lecciones.all()
        # Contamos cuántas lecciones tiene en total el módulo
        total_lecciones = lecciones.count()
        lecciones_completadas = 0

        # Recorremos cada lección del módulo actual
        for leccion in lecciones:
            if leccion.completada:          # estructura condicional if, verifica si se completó
                lecciones_completadas += 1  # Sumamos 1 al contador

        # Calculamos el porcentaje de progreso del módulo individual
        if total_lecciones > 0:
            modulo.progreso = int((lecciones_completadas / total_lecciones) * 100)
        else:
            modulo.progreso = 0

        # Un módulo está completo si tiene lecciones y todas están completadas
        modulo.esta_completo = (total_lecciones > 0 and lecciones_completadas == total_lecciones)

        # Un módulo se desbloquea solo si el anterior ya fue completado
        modulo.desbloqueado = modulo_anterior_completo
        # Actualizamos la variable para la siguiente iteración del ciclo (el próximo módulo)
        modulo_anterior_completo = modulo.esta_completo

        # Si el módulo actual está completo, sumamos 1 al total de módulos terminados
        if modulo.esta_completo:
            modulos_completados += 1

    # Obtenemos la cantidad total de módulos existentes
    total_modulos = modulos.count()
    # Calculamos el porcentaje de progreso general
    if total_modulos > 0:
        progreso_general = int((modulos_completados / total_modulos) * 100)
    else:
        progreso_general = 0

    # Estructura condicional if / elif / else para determinar el nivel del usuario en base a su progreso
    if progreso_general >= 76:
        nivel = 'Experto'
    elif progreso_general >= 51:
        nivel = 'Avanzado'
    elif progreso_general >= 26:
        nivel = 'Intermedio'
    else:
        nivel = 'Principiante'

    # Diccionario con todos los datos que enviaremos a la plantilla dashboard.html
    data = {
        'usuario': usuario,
        'modulos': modulos,
        'progreso_general': progreso_general,
        'nivel': nivel,
    }
    # Renderizamos la plantilla con el contexto preparado
    return render(request, 'dashboard.html', data)


def leccion_view(request, leccion_id):
    """
    Muestra una lección tipo "Mito o Verdad" y procesa la respuesta del usuario.
    Si la respuesta es correcta, marca la lección como completada.
    """
    # Buscamos la lección en la BD por su id. Si no existe, lanza error 404 (No Encontrado)
    leccion = get_object_or_404(Leccion, id=leccion_id)
    # Instanciamos el formulario para responder
    form = forms.RespuestaForm()
    resultado = None # Inicializamos el resultado como nulo (aún no responde)

    # Verificamos si el usuario envió el formulario
    if request.method == 'POST':
        # Pasamos los datos enviados al formulario
        form = forms.RespuestaForm(request.POST)
        if form.is_valid():
            # Extraemos la opción seleccionada ('verdad' o 'mito')
            respuesta = form.cleaned_data['respuesta']
            # Evaluamos si la respuesta del usuario significa 'True'
            respuesta_es_verdad = (respuesta == 'verdad')

            # Comparamos la respuesta del usuario con la respuesta real de la base de datos
            if respuesta_es_verdad == leccion.es_verdad:
                resultado = 'correcto'
                leccion.completada = True # Cambiamos el estado de la lección
                leccion.save() # Guardamos los cambios en la base de datos
            else:
                resultado = 'incorrecto'

    # Preparamos los datos para enviar a la vista de la lección
    data = {
        'leccion': leccion,
        'form': form,
        'resultado': resultado, # Enviamos si fue correcto, incorrecto o si aún no responde
    }
    # Renderizamos la página leccion.html
    return render(request, 'leccion.html', data)
