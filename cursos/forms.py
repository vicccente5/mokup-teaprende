from django import forms


class LoginForm(forms.Form):
    """Formulario simple de acceso a la plataforma (sin base de datos de usuarios)."""
    usuario = forms.CharField(
        label="Usuario",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tu nombre'})
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'})
    )


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
