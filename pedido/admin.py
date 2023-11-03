from django.contrib import admin

from .models import (DetallePedido, EstadoPedido, MetodoPago, Pedido)

admin.site.register(DetallePedido)
admin.site.register(EstadoPedido)
admin.site.register(MetodoPago)
admin.site.register(Pedido)

