from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# form para iniciar sesion
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )
    contrasena = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '********'})
    )

# form para el registro de los profes o papas (solo pide correo y pass)
class RegistroForm(UserCreationForm):
    username = None # ocultamos el username porque usaremos el correo
    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'ejemplo@correo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",) # la pass la pone django automatico

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # aca le pongo la clase de css a todos los inputs para que se vean bien
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})

    def clean_email(self):
        # validar que el correo termine en algo valido
        email = self.cleaned_data.get('email')
        if email:
            dominios = (".com", ".cl", ".net", ".org", ".edu")
            if not email.endswith(dominios):
                raise forms.ValidationError("Usa un correo valido por favor (.com, .cl)")
        
        # revisar si ya existe alguien con este correo
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
            
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email # guardamos el correo en el username para que django no reclame
        if commit:
            user.save()
        return user

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

