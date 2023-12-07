from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import EstadoPedido, DetallePedido, Pedido



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
        'estado_pedido': orden.estado_pedido.nombre if orden.estado_pedido else None,
        # Otros campos simples aquí...
    }
    
    return JsonResponse(data)

def actualizar_orden(request, orden_id):
    if request.method == 'POST':
        orden = get_object_or_404(Pedido, id=orden_id)

        nueva_fecha_envio = request.POST.get('fecha_envio')
        nuevo_estado_pedido_id = request.POST.get('estado_pedido')

        # Busca el objeto EstadoPedido por su ID
        estado_pedido = get_object_or_404(EstadoPedido, pk=nuevo_estado_pedido_id)

        # Actualiza la orden con los nuevos datos
        orden.fecha_de_envio = nueva_fecha_envio
        orden.estado_pedido = estado_pedido  # Asigna la instancia del EstadoPedido
        orden.save()

        return redirect('pedido:ordenes')  # Redirige a la URL de la lista de órdenes

    return JsonResponse({'mensaje': 'Error al actualizar la orden'})


def obtener_detalles_pedido(request, orden_id):
    orden = get_object_or_404(Pedido, id=orden_id)
    detalles_pedido = DetallePedido.objects.filter(pedido=orden)
    
    detalles = []
    for detalle in detalles_pedido:
        detalles.append({
            'producto_nombre': detalle.producto.nombre,
            'cantidad': detalle.cantidad,
            'precio_producto': detalle.precio_producto,
            'imagen_url': detalle.producto.imagen.url if detalle.producto.imagen else None,
            # Agrega más campos del detalle si es necesario
        })

    detalles_usuario = {
        'nombre': orden.usuario.name,
        'correo': orden.usuario.email,
        'direccion': orden.usuario.direccion,
        'pais': orden.usuario.ciudad.departamento.departamento.nombre if orden.usuario.ciudad else None,
        'ciudad': orden.usuario.ciudad.nombre if orden.usuario.ciudad else None,
        'departamento': orden.usuario.ciudad.departamento.nombre if orden.usuario.ciudad else None,
        # Agrega más campos del usuario si es necesario
    }
    
    data = {
        'detalles_pedido': detalles,
        'detalles_usuario': detalles_usuario  # Pasar detalles del usuario al contexto
    }
    
    return JsonResponse(data)



