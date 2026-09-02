from django.db import models


class Modulo(models.Model):
    """
    Representa un módulo de la ruta de aprendizaje de TeaAprende.
    Cada módulo agrupa una o más lecciones tipo "Mito o Verdad".
    """
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(help_text="Posición del módulo en la ruta de aprendizaje (1, 2, 3...)")
    icono = models.CharField(
        max_length=50,
        default='fa-solid fa-puzzle-piece',
        help_text="Clase de Font Awesome usada en el dashboard"
    )

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Módulo {self.orden}: {self.titulo}"


class Leccion(models.Model):
    """
    Lección tipo "Mito o Verdad" perteneciente a un módulo.
    El usuario debe indicar si la afirmación (pregunta) es verdadera o un mito.
    """
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    pregunta = models.CharField(max_length=300, help_text="Afirmación a evaluar como Mito o Verdad")
    es_verdad = models.BooleanField(help_text="True si la afirmación es VERDADERA, False si es un MITO")
    explicacion = models.TextField(help_text="Texto que se muestra al usuario luego de responder")
    completada = models.BooleanField(default=False, help_text="Indica si el usuario ya respondió correctamente")

    def __str__(self):
        return self.pregunta
