from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Clase encargada de manejar los datos de inicio de sesión de los usuarios.
# Captura el nombre de usuario y la contraseña introducidos en el login.
class LoginForm(forms.Form):
    """Formulario de acceso a la plataforma."""
    usuario = forms.CharField(
        label="Nombre de Usuario",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu usuario'})
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )


# Clase encargada de gestionar el registro de nuevos usuarios en el sistema.
# Hereda de UserCreationForm (el formulario nativo de Django) para aplicar automáticamente
# validaciones de seguridad de contraseña y crear el usuario en la base de datos,
# además de aplicarle las clases CSS de nuestro diseño.
class RegistroForm(UserCreationForm):
    """Formulario de registro que aplica los estilos de la app."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})


# Clase utilizada en la vista de cada lección individual.
# Su propósito es capturar la respuesta del usuario (Mito o Verdad) a través de un
# botón de radio para luego compararla con la respuesta correcta almacenada en el modelo.
class RespuestaForm(forms.Form):
    """Formulario usado dentro de una lección para responder Mito o Verdad."""
    OPCIONES = [
        ('verdad', 'Verdad'),
        ('mito', 'Mito'),
    ]
    respuesta = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.RadioSelect,
        label="¿Mito o Verdad?"
    )

