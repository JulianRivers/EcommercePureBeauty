from django.shortcuts import render

from .models import (Producto, ProductoSubcategoria, Subcategoria)

# Create your views here.

def index(request):
    return render(request, 'index.html')


def inicio(request):
    productos = Producto.objects.all()

    for producto in productos:
        if producto.precio_desc == producto.precio_act:
            producto.precio_desc = 0
        try:
            productoSubcategoria = ProductoSubcategoria.objects.get(producto=producto)
            producto.categoria = productoSubcategoria.subcategoria
        except ProductoSubcategoria.DoesNotExist:
            producto.categoria = 'Sin categoría'

    return render(request, 'productos.html', {'productos': productos})
