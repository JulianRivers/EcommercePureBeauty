from django.shortcuts import render, redirect

from .models import (Producto, ProductoSubcategoria, Subcategoria)
from .forms import (ProductoForm, ProductoSubcategoriaForm)
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
            
    context = {
        'productos': productos, 
        'form_producto':ProductoForm(), 
        'form_subcategoria': ProductoSubcategoriaForm(),
    }
    return render(request, 'productos.html', context)

def addProducto(request):
    if request.method == 'POST':
        print('hola')
        form_producto = ProductoForm(request.POST)
        form_subcategoria = ProductoSubcategoriaForm(request.POST)

        if form_producto.is_valid() and form_subcategoria.is_valid():
            # Guarda el producto
            producto = form_producto.save()

            # Guarda la relación ProductoSubcategoria
            producto_subcategoria = form_subcategoria.save(commit=False)
            producto_subcategoria.producto = producto
            producto_subcategoria.save()

            return redirect('usuario:index')
    return render(request, 'productos.html',)
