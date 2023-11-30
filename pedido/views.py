from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Pedido
from .models import EstadoPedido


# Create your views here.
def index(request):
    return render(request, 'index.html')


def lista_ordenes(request):
    # Obtener todas las órdenes de la base de datos
    ordenes = Pedido.objects.all()
    
    # Obtener todos los estados de pedido
    estados_pedidos = EstadoPedido.objects.all()

    return render(request, 'ordenes.html', {'ordenes': ordenes, 'estados_pedidos': estados_pedidos})

def obtener_orden(request, orden_id):
    orden = get_object_or_404(Pedido, id=orden_id)
    data = {
        'id': orden.id,
        'fecha_de_envio': orden.fecha_de_envio.strftime('%Y-%m-%d') if orden.fecha_de_envio else None,
        'estado_pedido': orden.estado_pedido.nombre,  # Suponiendo que 'nombre' es un campo de EstadoPedido
        # Otros campos simples aquí...
    }
    return JsonResponse(data)

def actualizar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Pedido, id=orden_id)

        nueva_fecha_envio = request.POST.get('fecha_envio')
        nuevo_estado_pedido_id = request.POST.get('estado_pedido')

        # Busca el objeto EstadoPedido por su ID
        estado_pedido = EstadoPedido.objects.get(pk=nuevo_estado_pedido_id)

        # Actualiza la orden con los nuevos datos
        orden.fecha_de_envio = nueva_fecha_envio
        orden.estado_pedido = estado_pedido  # Asigna la instancia del EstadoPedido
        orden.save()

        return JsonResponse({'mensaje': 'Orden actualizada correctamente'})

    return JsonResponse({'mensaje': 'Error al actualizar la orden'})