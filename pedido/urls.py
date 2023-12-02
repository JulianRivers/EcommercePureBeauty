from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="pedido"
urlpatterns = [
    path('ordenes/', views.lista_ordenes, name='ordenes'),
    path('obtener_orden/<int:orden_id>/', views.obtener_orden, name='obtener_orden'),
    path('obtener_detalles_pedido/<int:orden_id>/', views.obtener_detalles_pedido, name='obtener_detalles'),
    path('actualizar_orden/<int:orden_id>/', views.actualizar_orden, name='actualizar_orden'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)