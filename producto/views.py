import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import (Producto, ProductoSubcategoria)
from .forms import (ProductoForm, ProductoSubcategoriaForm)
# Create your views here.

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
        form_producto = ProductoForm(request.POST, request.FILES)
        form_subcategoria = ProductoSubcategoriaForm(request.POST)

        if form_producto.is_valid() and form_subcategoria.is_valid():
            producto = form_producto.save(commit=False)
            producto.is_activo = True
            producto.precio_desc = producto.precio_act
            producto.fecha_inicio_desc = timezone.now()
            producto.fecha_fin_desc = timezone.now()
            producto.ult_actualizacion = timezone.now()
            print(request.FILES)

            producto.imagen = request.FILES['imagen']
            print(producto.imagen)
            producto.save()

            producto_subcategoria = form_subcategoria.save(commit=False)
            producto_subcategoria.producto = producto
            producto_subcategoria.save()

            return redirect('producto:inicio')
    return render(request, 'productos.html',)