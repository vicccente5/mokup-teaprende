from django.db import migrations

# Contenido inicial de la ruta de aprendizaje de TeaAprende.
# Cada módulo trae asociadas una o más lecciones tipo "Mito o Verdad".
MODULOS = [
    {
        'titulo': 'Introducción al TEA',
        'descripcion': '¿Qué es el Trastorno del Espectro Autista y cómo entender su diversidad?',
        'orden': 1,
        'icono': 'fa-solid fa-puzzle-piece',
        'lecciones': [
            {
                'pregunta': 'El TEA es una enfermedad que se puede curar con tratamiento médico.',
                'es_verdad': False,
                'explicacion': 'El TEA no es una enfermedad: es una condición del neurodesarrollo. '
                                'No se "cura", se acompaña, se comprende y se apoya durante toda la vida.',
            },
        ],
    },
    {
        'titulo': 'Comunicación y Empatía',
        'descripcion': 'Mitos y verdades sobre la comunicación e interacción social.',
        'orden': 2,
        'icono': 'fa-solid fa-comments',
        'lecciones': [
            {
                'pregunta': 'Todas las personas con TEA tienen los mismos desafíos sensoriales.',
                'es_verdad': False,
                'explicacion': 'Cada persona con TEA es única. Mientras algunos pueden ser '
                                'hipersensibles al ruido o a las luces, otros pueden ser hiposensibles.',
            },
            {
                'pregunta': 'El contacto visual puede resultar incómodo o abrumador para algunas personas con TEA.',
                'es_verdad': True,
                'explicacion': 'Muchas personas con TEA experimentan el contacto visual como algo '
                                'intenso; evitarlo no significa desinterés ni falta de respeto.',
            },
        ],
    },
    {
        'titulo': 'Sensorialidad y Entorno',
        'descripcion': 'Comprendiendo los desafíos de integración sensorial en el aula.',
        'orden': 3,
        'icono': 'fa-solid fa-ear-listen',
        'lecciones': [
            {
                'pregunta': 'Los ruidos fuertes o las luces intensas pueden generar mucho malestar en personas con TEA.',
                'es_verdad': True,
                'explicacion': 'La hipersensibilidad sensorial es muy común en personas con TEA; '
                                'adaptar el entorno (luz, sonido) puede mejorar mucho su bienestar.',
            },
        ],
    },
    {
        'titulo': 'Estrategias en el Aula',
        'descripcion': 'Herramientas prácticas para profesores y educadores diferenciales.',
        'orden': 4,
        'icono': 'fa-solid fa-chalkboard-user',
        'lecciones': [
            {
                'pregunta': 'Usar rutinas claras y anticipar los cambios ayuda a reducir la ansiedad en estudiantes con TEA.',
                'es_verdad': True,
                'explicacion': 'La anticipación y las rutinas predecibles entregan seguridad y '
                                'reducen significativamente los niveles de ansiedad y estrés.',
            },
        ],
    },
    {
        'titulo': 'Evaluación Final',
        'descripcion': 'Demuestra lo aprendido y obtén tu certificado de Inclusión TEA.',
        'orden': 5,
        'icono': 'fa-solid fa-certificate',
        'lecciones': [
            {
                'pregunta': 'Aprender sobre el TEA solo es útil para profesores y profesionales de la salud.',
                'es_verdad': False,
                'explicacion': 'Familias, empleadores y la sociedad en general se benefician de '
                                'conocer el TEA: la inclusión es responsabilidad de todos.',
            },
        ],
    },
]


def crear_datos_iniciales(apps, schema_editor):
    """Crea los módulos y lecciones de ejemplo la primera vez que se migra el proyecto."""
    Modulo = apps.get_model('cursos', 'Modulo')
    Leccion = apps.get_model('cursos', 'Leccion')

    for modulo_data in MODULOS:
        lecciones_data = modulo_data.pop('lecciones')
        modulo = Modulo.objects.create(**modulo_data)
        for leccion_data in lecciones_data:
            Leccion.objects.create(modulo=modulo, **leccion_data)


def eliminar_datos_iniciales(apps, schema_editor):
    """Permite revertir la migración (django-admin migrate cursos 0001)."""
    Modulo = apps.get_model('cursos', 'Modulo')
    Modulo.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, eliminar_datos_iniciales),
    ]
