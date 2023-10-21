from django.urls import path
from . import views

app_name="empleado"
urlpatterns = [
    path('inicio', views.inicio, name="inicio"),
    path('registro', views.registerView, name="registro"),
    path('evento/<int:idEvento>', views.evento, name="evento"),
    path('evento/<int:idEvento>/agregar/', views.agregarViatico, name="agregarViatico"),
]

