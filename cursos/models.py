from django.db import models # Importa el módulo de base de datos de Django para crear modelos

# Definición del modelo 'Modulo' que representa una sección del curso
class Modulo(models.Model):
    """
    Representa un módulo de la ruta de aprendizaje de TeaAprende.
    Cada módulo agrupa una o más lecciones tipo "Mito o Verdad".
    """
    # Campo de texto para el título del módulo, con un máximo de 200 caracteres
    titulo = models.CharField(max_length=200)
    
    # Campo de texto largo para la descripción detallada del módulo
    descripcion = models.TextField()
    
    # Campo numérico positivo para establecer el orden del módulo (1, 2, 3...)
    orden = models.PositiveIntegerField(help_text="Posición del módulo en la ruta de aprendizaje (1, 2, 3...)")
    
    # Campo de texto corto que almacena la clase CSS del icono de Font Awesome
    icono = models.CharField(
        max_length=50,
        default='fa-solid fa-puzzle-piece', # Icono por defecto
        help_text="Clase de Font Awesome usada en el dashboard"
    )

    # Subclase Meta para configuraciones adicionales del modelo
    class Meta:
        # Define que, por defecto, los módulos se ordenarán por el campo 'orden'
        ordering = ['orden']

    # Método mágico que define cómo se representa el objeto como una cadena de texto (string)
    def __str__(self):
        return f"Módulo {self.orden}: {self.titulo}"


# Definición del modelo 'Leccion' que representa una pregunta dentro de un módulo
class Leccion(models.Model):
    """
    Lección tipo "Mito o Verdad" perteneciente a un módulo.
    El usuario debe indicar si la afirmación (pregunta) es verdadera o un mito.
    """
    # Relación de muchos a uno: Cada lección pertenece a un único módulo.
    # on_delete=models.CASCADE significa que si se borra el módulo, se borran sus lecciones.
    # related_name='lecciones' permite acceder a las lecciones desde un objeto módulo (modulo.lecciones.all())
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    
    # Campo de texto para la afirmación o pregunta de la lección
    pregunta = models.CharField(max_length=300, help_text="Afirmación a evaluar como Mito o Verdad")
    
    # Campo booleano (Verdadero/Falso) que indica la respuesta correcta
    es_verdad = models.BooleanField(help_text="True si la afirmación es VERDADERA, False si es un MITO")
    
    # Campo de texto largo que contiene la justificación o respuesta explicada
    explicacion = models.TextField(help_text="Texto que se muestra al usuario luego de responder")
    
    # Campo booleano que registra si el usuario ha completado correctamente la lección (por defecto es False)
    completada = models.BooleanField(default=False, help_text="Indica si el usuario ya respondió correctamente")

    # Método que define la representación en texto de la lección (se mostrará la pregunta)
    def __str__(self):
        return self.pregunta
