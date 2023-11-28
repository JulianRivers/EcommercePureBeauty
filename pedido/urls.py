from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="pedido"
urlpatterns = [
    path('/ordenes',views.index, name='ordenes'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)