import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import (Producto, ProductoSubcategoria, Subcategoria)
from .forms import (ProductoForm, ProductoSubcategoriaForm)
# Create your views here.

def inicio(request):
    productos = Producto.objects.all()

    for producto in productos:
        if producto.precio_desc == producto.precio_act:
            producto.precio_desc = 0
        try:
            productoSubcategoria = ProductoSubcategoria.objects.filter(producto=producto).first()
            producto.categoria = productoSubcategoria.subcategoria
        except ProductoSubcategoria.DoesNotExist:
            producto.categoria = 'Sin categoría'
            
    context = {
        'productos': productos, 
        'form_producto':ProductoForm(), 
        'form_subcategoria': ProductoSubcategoriaForm(),
    }
    return render(request, 'productos.html', context)

def categoria(request):
    productos = Subcategoria.objects.all()

            
    context = {
        'productos': productos, 
        'form_producto':ProductoForm(), 
        'form_subcategoria': ProductoSubcategoriaForm(),
    }
    return render(request, 'categorias.html', context)

def agregar_categoria(request):
    productos = Subcategoria.objects.all()
  
    context = {
        'productos': productos, 
        'form_producto':ProductoForm(), 
        'form_subcategoria': ProductoSubcategoriaForm(),
    }
    return render(request, 'categorias_add.html', context)

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

def detalleProducto(request, id):
    productos = Producto.objects.all()
    detalle = get_object_or_404(Producto, id=id)

    for producto in productos:
        if producto.precio_desc == producto.precio_act:
            producto.precio_desc = 0
        try:
            productoSubcategorias = ProductoSubcategoria.objects.filter(producto=detalle)
            categorias = [subcategoria.subcategoria for subcategoria in productoSubcategorias]
        except ProductoSubcategoria.DoesNotExist:
             categorias = ['Sin categoría']
    print(categorias)
    context = {
        'productos': productos,
        'detalle': detalle,
        'categorias': categorias
    }
    return render(request, 'productos_detalle.html', context)

def deleteProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('producto:inicio')

def editarProducto(request, id):
    # Obtén el producto por ID
    producto = get_object_or_404(Producto, id=id)
    productos = Producto.objects.all()
    if request.method == 'POST':
        # Llena los formularios con los datos existentes del producto
        form_producto = ProductoForm(request.POST, request.FILES, instance=producto)
        form_subcategoria = ProductoSubcategoriaForm(request.POST)

        if form_producto.is_valid() and form_subcategoria.is_valid():
            # Guarda los cambios en el producto
            producto = form_producto.save(commit=False)
            producto.is_activo = True
            producto.precio_desc = producto.precio_act
            producto.fecha_inicio_desc = timezone.now()
            producto.fecha_fin_desc = timezone.now()
            producto.ult_actualizacion = timezone.now()
            producto.imagen = request.FILES.get('imagen', producto.imagen)  # Si no se proporciona nueva imagen, usa la existente
            producto.save()
            if 'subcategoria' in form_subcategoria.cleaned_data and form_subcategoria.cleaned_data['subcategoria'] is not None:
                producto_subcategoria = form_subcategoria.save(commit=False)
                producto_subcategoria.producto = producto
                producto_subcategoria.save()  

            return redirect('producto:inicio')

    # Llena los formularios con los datos existentes del producto
    context = {
        'productos': productos,
        'detalle': producto,
        'form_producto' : ProductoForm(instance=producto),
        'form_subcategoria' : ProductoSubcategoriaForm(),
    }

    return render(request, 'productos_editar.html', context)