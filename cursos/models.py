from django.db import models

# este es el modelo para los modulos del curso (como los temas)
class Modulo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.PositiveIntegerField() # aca guardamos el orden 1, 2, 3...
    icono = models.CharField(max_length=50, default='fa-solid fa-puzzle-piece')
    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f"Módulo {self.orden}: {self.titulo}"

# esta tabla es para cada pregunta de verdadero o falso que va dentro del modulo
class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    pregunta = models.CharField(max_length=300)
    es_verdad = models.BooleanField() # true si es verdad, false si es un mito
    explicacion = models.TextField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.pregunta
