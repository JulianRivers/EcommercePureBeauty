from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="usuario"
urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.loginView, name='login'),
    path('logout', views.logoutView, name="logout"),
    path('registro', views.registerView, name='registro'),
    path('clientes', views.registerView, name='clientes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)