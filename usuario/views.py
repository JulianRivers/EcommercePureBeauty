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

        # Obtener los datos de imagen para cada producto en el carrito
        productos_con_imagen = []
        for producto_en_carrito in productos_en_carrito:
            imagen_url = producto_en_carrito.producto.imagen.url if producto_en_carrito.producto.imagen else None
            producto_con_imagen = {
                'producto': producto_en_carrito.producto,
                'cantidad': producto_en_carrito.cantidad,
                'imagen_url': imagen_url
            }
            productos_con_imagen.append(producto_con_imagen)

        nombre_cliente = cliente.name  # Obtener el nombre del cliente

    except (UserProfile.DoesNotExist, Carrito.DoesNotExist):
        # Si el usuario o el carrito no existen, asignamos una lista vacía de productos
        nombre_cliente = ""  # Si no se encuentra el cliente, asignar cadena vacía
        productos_con_imagen = []

    return render(request, 'carritoDeCompras.html', {'productos_en_carrito': productos_con_imagen, 'nombre_cliente': nombre_cliente})

