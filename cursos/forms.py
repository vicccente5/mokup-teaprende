# Importamos el módulo forms de Django, que nos ayuda a crear formularios HTML de manera segura
from django import forms


class LoginForm(forms.Form):
    """Formulario simple de acceso a la plataforma (sin base de datos de usuarios reales)."""
    
    # Campo de texto para el nombre de usuario
    usuario = forms.CharField(
        label="Usuario", # Etiqueta que se mostrará junto al campo en el HTML
        max_length=100, # Límite de caracteres
        # Configuración del widget (la representación HTML del campo)
        # Permite agregar clases CSS y otros atributos como el 'placeholder' (texto fantasma)
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu nombre'})
    )
    
    # Campo para la contraseña (aunque no se use en BD en este proyecto, sirve de simulación)
    contrasena = forms.CharField(
        label="Contraseña",
        # PasswordInput hace que el texto escrito se oculte con asteriscos (type="password" en HTML)
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )


class RespuestaForm(forms.Form):
    """Formulario usado dentro de una lección para responder Mito o Verdad."""
    
    # Lista de tuplas con las opciones disponibles (valor_interno, Etiqueta_mostrada)
    OPCIONES = [
        ('verdad', 'Verdad'),
        ('mito', 'Mito'),
    ]
    
    # Campo de opción múltiple, donde el usuario solo puede elegir una opción
    respuesta = forms.ChoiceField(
        choices=OPCIONES, # Asignamos las opciones definidas arriba
        widget=forms.RadioSelect, # RadioSelect lo dibuja como botones de radio (bolitas seleccionables) en HTML
        label="¿Mito o Verdad?"
    )
