from django.contrib import admin

from .models import (DetallePedido, EstadoPedido, MetodoPago, Pedido)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    pass

@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    pass