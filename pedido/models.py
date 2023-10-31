from django.db import models
from usuario.models import UserProfile as Usuario
from producto.models import Producto

# Modelos de la base de datos relacionados con los pedidos

class MetodoPago (models.Model):
    '''Modelo que representa la tabla en la BD de los métodos de pago'''
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        '''Representación en un String del método de pago'''
        return f"Método: {self.nombre}"


class EstadoPedido(models.Model):
    '''Modelo que representa el estado de los pedidos: En espera, Entregado, etc.'''

    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        '''Representación en un String del Estado del Pedido'''
        return self.nombre


class Pedido(models.Model):
    '''Modelo que representa los pedidos de un usuario.'''

    direccion_entrega = models.CharField('Dirección de entrega', max_length=500)
    fecha = models.DateTimeField('Fecha del pedido')
    total_compra = models.DecimalField('Precio total de la compra', max_digits=15, decimal_places=2)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')
    metodo = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, verbose_name='Método de pago')
    estado_pedido = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE, verbose_name='Estado de pedido')

    def __str__(self):
        ''' Obtener cadena representativa de el Pedido '''
        return f"Pedido {self.id} por {self.usuario.name} fecha: {self.fecha}"


class DetallePedido(models.Model):
    '''Modelo para persistir el histórico de los productos'''
    pedido = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, verbose_name='Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    precio_producto = models.DecimalField('Precio del Producto', max_digits=15, decimal_places=2)
    cantidad = models.PositiveIntegerField('Cantidad')

    def __str__(self):
        ''' Obtener cadena representativa del detalle del pedido '''
        return f"Pedido {self.pedido.id} del producto {self.producto.nombre} "
