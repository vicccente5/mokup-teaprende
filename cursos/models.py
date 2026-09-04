from django.db import models

# Modelo que representa una sección principal o "Módulo" en la ruta de aprendizaje.
# Sirve para agrupar varias lecciones bajo un mismo tema, manteniendo un orden lógico,
# un título, una descripción y un ícono representativo para mostrar en el panel.
class Modulo(models.Model):
    """Representa un módulo de la ruta de aprendizaje."""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField(help_text="Posición del módulo (1, 2, 3...)")
    icono = models.CharField(
        max_length=50,
        default='fa-solid fa-puzzle-piece',
        help_text="Clase de Font Awesome"
    )

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Módulo {self.orden}: {self.titulo}"


# Modelo que representa una pregunta o "Lección" individual de tipo Mito o Verdad.
# Está fuertemente vinculada a un Módulo específico mediante una llave foránea.
# Almacena la afirmación, la respuesta correcta, la explicación posterior y su estado de completitud.
class Leccion(models.Model):
    """Lección tipo 'Mito o Verdad' perteneciente a un módulo."""
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    pregunta = models.CharField(max_length=300)
    es_verdad = models.BooleanField(help_text="True si es VERDADERA, False si es un MITO")
    explicacion = models.TextField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.pregunta
