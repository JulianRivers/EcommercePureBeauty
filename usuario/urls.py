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
    path('detalle_producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('nuevos',views.nuevos, name='nuevos'),
    path('productos/<int:subcategoria_id>/', views.productos_por_subcategoria, name='productos_por_subcategoria'),
    path('agregar-a-lista-deseos/<int:producto_id>/', views.agregar_a_lista_deseos, name='agregar_a_lista_deseos'),
    path('verificar-lista-deseos/<int:producto_id>/', views.verificar_lista_deseos, name='verificar_lista_deseos'),
    path('lista-deseos/', views.lista_deseos, name='lista_deseos'),
    path('perfil',views.perfil, name='perfil'),
    path('perfil/datos',views.editar_datos, name='datos'),
    path('perfil/password',views.change_password, name='change'),
    path('carrito_compra_cliente/', views.carrito_compra_cliente, name='carrito_compra_cliente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)