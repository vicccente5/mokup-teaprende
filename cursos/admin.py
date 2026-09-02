from django.contrib import admin
from .models import Modulo, Leccion


class LeccionInline(admin.TabularInline):
    model = Leccion
    extra = 1


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('orden', 'titulo')
    inlines = [LeccionInline]


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'modulo', 'es_verdad', 'completada')
