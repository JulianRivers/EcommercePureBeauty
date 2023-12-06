from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="producto"
urlpatterns = [
    path('productos',views.inicio, name='inicio'),
    path('producto/add',views.addProducto, name='add'),
    path('producto/<int:id>', views.detalleProducto, name='detalle'),
    path('producto/delete/<int:id>', views.deleteProducto, name='delete'),
    path('categorias',views.index, name='categorias'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)