"""
URL configuration for teaaprende project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
# Importamos el módulo admin para habilitar el panel de administración de Django
from django.contrib import admin
# Importamos la función path, que nos permite definir las rutas (URLs) de la aplicación
from django.urls import path
# Importamos las vistas (funciones) que creamos en nuestra aplicación 'cursos'
from cursos.views import login_view, dashboard_view, leccion_view

# Lista que contiene todas las rutas (URLs) disponibles en el proyecto
urlpatterns = [
    # Ruta para el panel de administración (ej: misitio.com/admin/)
    path('admin/', admin.site.urls),
    
    # Ruta raíz (ej: misitio.com/). Está vacía (''). Apunta a la vista de login.
    # El parámetro name='login' nos permite referenciar esta ruta desde el código o las plantillas HTML
    path('', login_view, name='login'),
    
    # Ruta para el dashboard (ej: misitio.com/dashboard/). Apunta a dashboard_view.
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Ruta dinámica para las lecciones (ej: misitio.com/leccion/1/, misitio.com/leccion/2/)
    # <int:leccion_id> captura el número en la URL y se lo pasa a la vista 'leccion_view' como argumento
    path('leccion/<int:leccion_id>/', leccion_view, name='leccion'),
]
