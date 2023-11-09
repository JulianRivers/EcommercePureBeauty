from django.db import models
from usuario.models import Carrito

# Modelos de la base de datos relacionados con los productos


class Producto (models.Model):
    '''Modelo que representa la tabla en la BD de los productos'''
    nombre = models.CharField('Nombre', max_length=100)
    stock = models.PositiveIntegerField('Stock')
    descripcion = models.CharField('Descripcion', max_length=500)
    is_activo = models.BooleanField('Es un producto activo')
    precio_act = models.DecimalField('Precio', max_digits=15, decimal_places=2)
    precio_desc = models.DecimalField('Precio con descuento', max_digits=15, decimal_places=2)
    fecha_inicio_desc = models.DateTimeField('Fecha incio del descuento')
    fecha_fin_desc = models.DateTimeField('Fecha finalización del descuento')
    ult_actualizacion = models.DateTimeField('Fecha últ. actualización')
    imagen = models.ImageField('Imagen del producto', upload_to='productos/', blank=True, null=True)

    def __str__(self):
        '''Representación en un String del producto'''
        return f"Producto: {self.nombre}"


class Categoria(models.Model):
    ''' Modelo que respresenta las categorías generales de los productos'''
    nombre = models.CharField('Nombre', max_length=100)
    categoria_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='categorias_hijas')


    def __str__(self):
        '''Representación en un String de la Categoria'''
        return self.get_nombre_completo()

    def get_nombre_completo(self):
        if self.categoria_padre:
            # Si tiene una categoría padre, llamamos recursivamente al método get_nombre_completo
            return f"{self.categoria_padre.get_nombre_completo()} > {self.nombre}"
        else:
            # Si no tiene una categoría padre, retorna solo el nombre
            return self.nombre


class Subcategoria(models.Model):
    ''' Modelo que respresenta las categorias particulares/individuales de los productos'''
    nombre = models.CharField('Nombre', max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        '''Representación en un String de la subcategoria'''
        return f"{self.categoria} > {self.nombre}"
    


class ProductoSubcategoria(models.Model):
    ''' Modelo que respresenta la relación muchos a muchos entre producto y categorias'''
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)

    def __str__(self):
        '''Representación en un String de la relación'''
        return f"producto: {self.producto.nombre} categoria:{self.subcategoria.nombre}"

class ProductoEnCarrito(models.Model):
    ''' Modelo que respresenta la relación muchos a muchos entre producto y categorias'''
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField('Cantidad del producto en carrito')

    def __str__(self):
        '''Representación en un String de la relación'''
        return f"producto: {self.producto.nombre} cantidad: {self.cantidad} carrito de:{self.carrito.usuario.name}"

