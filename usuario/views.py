from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import (UserProfile, Carrito)
from producto.models import ProductoEnCarrito
from .forms import (LoginForm, RegistroForm)

def loginView(request):
    if request.user.is_superuser:
        return redirect('/admin')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = UserProfile.objects.get(email=email)
            if usuario is not None and usuario.check_password(password):
                login(request, usuario)
                return redirect('/admin') if usuario.is_superuser else redirect('producto:inicio')
            else:
                messages.error(request, "Contraseña incorrecta")
        except Exception as e:
            messages.error( request, "Lo sentimos, no pudimos encontrar tu cuenta")
            usuario = None
            print(e)
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def index(request):
    return render(request, 'index.html')

def logoutView(request):
    logout(request)
    return redirect('usuario:index')

def registerView(request):
    if not request.user.is_anonymous: 
        messages.error(request, "Cierre sesión antes de registrar otro usuario.")
        return redirect('usuario:index')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')  # Recuperar el valor del campo "password"
            usuario = form.save(commit=False)
            usuario.set_password(password)
            usuario.save()
            return redirect('usuario:login')        
    else:
        form = RegistroForm()
    context = {
        'form': form,
    }
    return render(request, 'registro.html', context)


def lista_clientes(request):
    clientes = UserProfile.objects.exclude(is_superuser=True)
    
    return render(request, 'clientes.html', {'clientes' : clientes})

def carrito_compras(request, cliente_id):
    try:
        cliente = UserProfile.objects.get(pk=cliente_id)
        carrito_usuario = Carrito.objects.get(usuario=cliente)
        productos_en_carrito = ProductoEnCarrito.objects.filter(carrito=carrito_usuario)

        total_compra = 0  # Inicializar el total de la compra
        productos_con_info = []

        for producto_en_carrito in productos_en_carrito:
            imagen_url = producto_en_carrito.producto.imagen.url if producto_en_carrito.producto.imagen else None
            precio_total = producto_en_carrito.producto.precio_act * producto_en_carrito.cantidad  # Precio * Cantidad
            producto_con_info = {
                'producto': producto_en_carrito.producto,
                'cantidad': producto_en_carrito.cantidad,
                'imagen_url': imagen_url,
                'precio': producto_en_carrito.producto.precio_act,
                'precio_total': precio_total  # Precio total del producto
            }
            total_compra += precio_total  # Sumar al total de la compra
            productos_con_info.append(producto_con_info)

        nombre_cliente = cliente.name

    except (UserProfile.DoesNotExist, Carrito.DoesNotExist):
        nombre_cliente = ""
        total_compra = 0
        productos_con_info = []

    return render(request, 'carritoDeCompras.html', {'productos_en_carrito': productos_con_info, 'nombre_cliente': nombre_cliente, 'total_compra': total_compra})

