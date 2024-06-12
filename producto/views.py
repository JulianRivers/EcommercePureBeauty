import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import (Producto, ProductoSubcategoria, Subcategoria)
from .forms import (ProductoForm, ProductoSubcategoriaForm, CategoriaForm)

@login_required(login_url='/login') 
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

@login_required(login_url='/login') 
def categoria(request):
    productos = Subcategoria.objects.all()

    context = {
        'productos': productos, 
    }
    return render(request, 'categorias.html', context)

@login_required(login_url='/login') 
def agregar_categoria(request):
    productos = Subcategoria.objects.all()

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto:categorias')
  
    context = {
        'productos': productos, 
        'form': CategoriaForm()
    }
    return render(request, 'categorias_add.html', context)

@login_required(login_url='/login') 
def deleteCategoria(request, id):
    print("SIUUUUU")
    categoria = get_object_or_404(Subcategoria, id=id)
    categoria.delete()
    return redirect('producto:categorias')

@login_required(login_url='/login') 
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

            # Procesa el campo tiene_iva para calcular el precio con IVA
            if form_producto.cleaned_data.get('tiene_iva'):
                producto.precio_act = producto.precio_act * Decimal('1.19')

            producto.imagen = request.FILES['imagen']
            producto.save()

            producto_subcategoria = form_subcategoria.save(commit=False)
            producto_subcategoria.producto = producto
            producto_subcategoria.save()

            return redirect('producto:inicio')
    else:
        form_producto = ProductoForm()
        form_subcategoria = ProductoSubcategoriaForm()

    return render(request, 'productos.html', {
        'form_producto': form_producto,
        'form_subcategoria': form_subcategoria,
    })

@login_required(login_url='/login') 
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

@login_required(login_url='/login') 
def deleteProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('producto:inicio')

@login_required(login_url='/login') 
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