from django.contrib import admin
from django.urls import path
from cursos.views import login_view, dashboard_view, leccion_view, register_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('registro/', register_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('leccion/<int:leccion_id>/', leccion_view, name='leccion'),
]

