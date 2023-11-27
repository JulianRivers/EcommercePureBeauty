from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="usuario"
urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.loginView, name='login'),
    path('logout', views.logoutView, name="logout"),
    path('dashboard', views.dashboardView, name='dashboard'),
    path('registro', views.registerView, name='registro'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)