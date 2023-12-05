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
    path('clientes', views.lista_clientes, name='clientes'),
    path('carrito/<int:cliente_id>/', views.carrito_compras, name='carritoDeCompras'),
    path('pedidos/<int:cliente_id>/', views.pedidos_cliente, name='pedidos_cliente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)