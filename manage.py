#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# Importamos el módulo os para interactuar con el sistema operativo
import os
# Importamos sys para manejar los argumentos pasados por la línea de comandos (terminal)
import sys


def main():
    """Run administrative tasks."""
    # Le indica a Django dónde encontrar la configuración del proyecto (settings.py)
    # En este caso, el archivo está en la carpeta teaaprende y se llama settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teaaprende.settings')
    try:
        # Importamos la función encargada de ejecutar comandos de Django (como runserver, migrate, etc)
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o no se encuentra en el entorno virtual, lanza este error
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando pasado por la terminal (ej. sys.argv sería ['manage.py', 'runserver'])
    execute_from_command_line(sys.argv)

# Punto de entrada principal del script. Si se ejecuta directamente, llama a la función main()
if __name__ == '__main__':
    main()
