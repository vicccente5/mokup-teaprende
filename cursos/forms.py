# Importamos el módulo forms de Django, que nos ayuda a crear formularios HTML de manera segura
from django import forms


class LoginForm(forms.Form):
    """Formulario de acceso a la plataforma con verificación de datos."""
    
    # Utilizamos EmailField para que Django valide automáticamente el formato del correo
    usuario = forms.EmailField(
        label="Correo Electrónico",
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
    
    # Campo para la contraseña
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )

    def clean_contrasena(self):
        """Verificación y validación de la contraseña."""
        contrasena = self.cleaned_data.get('contrasena')
        # Integración de validación de datos: comprobamos que la contraseña tenga un mínimo de seguridad
        if contrasena and len(contrasena) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return contrasena

    def clean_usuario(self):
        """Verificación adicional para el correo electrónico (usuario)."""
        correo = self.cleaned_data.get('usuario')
        # Se pueden agregar más integraciones aquí (por ejemplo, comprobar si el correo existe en la base de datos)
        if correo and not correo.endswith(".com") and not correo.endswith(".cl") and not correo.endswith(".net") and not correo.endswith(".org"):
            raise forms.ValidationError("Por favor, ingresa un dominio de correo válido (.com, .cl, .net, etc).")
        return correo


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
