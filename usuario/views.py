from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import (UserProfile, Carrito)
from producto.models import (ProductoEnCarrito, Producto, Subcategoria)
from pedido.models import Pedido, DetallePedido
from .forms import (LoginForm, RegistroForm, UsuarioForm, CambiarPasswordForm)
from django.http import HttpResponseRedirect
def loginView(request):
    if request.user.is_superuser:
        return redirect('producto:inicio')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = UserProfile.objects.get(email=email)
            if usuario is not None and usuario.check_password(password):
                login(request, usuario)
                return redirect('producto:inicio') if usuario.is_superuser else redirect('usuario:index')
            else:
                messages.error(request, "Contraseña incorrecta")
        except Exception as e:
            messages.error( request, "Lo sentimos, no pudimos encontrar tu cuenta")
            usuario = None
            print(e)
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def index(request):
    # Obtener todos los productos activos
    productos_todos = Producto.objects.filter(is_activo=True)

    # Obtener los primeros 5 productos con la fecha de actualización más reciente
    productos_recientes = Producto.objects.filter(is_activo=True).order_by('-ult_actualizacion')[:8]
    
    # Pasar los productos al contexto del template
    context = {
        'productos_todos': productos_todos,
        'productos_recientes': productos_recientes,
    }
    
    context.update(subcategorias(request))

    # Renderizar el template con los productos
    return render(request, 'index.html', context)


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

def pedidos_cliente(request, cliente_id):
    try:
        cliente = UserProfile.objects.get(pk=cliente_id)
        pedidos = Pedido.objects.filter(usuario=cliente)
        detalles_pedidos = []

        for pedido in pedidos:
            detalles_pedido = DetallePedido.objects.filter(pedido=pedido)
            
            detalles_pedidos.append({
                'pedido': pedido,
                'detalles': detalles_pedido,
                'total': sum(detalle.precio_producto * detalle.cantidad for detalle in detalles_pedido)
            })

    except UserProfile.DoesNotExist:
        detalles_pedidos = []

    return render(request, 'pedidos_cliente.html', {'detalles_pedidos': detalles_pedidos, 'cliente': cliente})

# metodo para mostrar el detalle de un producto
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidades = range(1, producto.stock + 1)
    context = {
        'producto': producto,
        'cantidades': cantidades,
    }
    return render(request, 'detalle_producto.html', context)


def nuevos(request):
    # Obtener los primeros 8 productos con la fecha de actualización más reciente
    productos_recientes = Producto.objects.filter(is_activo=True).order_by('-ult_actualizacion')[:8]
    # Pasar los productos al contexto del template
    context = {
        'productos_recientes': productos_recientes
    }
    
    context.update(subcategorias(request))
    
    # Renderizar el template con los productos
    return render(request, 'nuevos.html', context)

def perfil(request):
    usuario = request.user
    form = UsuarioForm(instance=usuario)
    form1 = CambiarPasswordForm()

    context = {
        "form": form,
        "form1": form1
    }
    
    
    context.update(subcategorias(request))
    
    # Renderizar el template con los productos
    return render(request, 'perfil.html', context)

def editar_datos(request):
    usuario = request.user
    form1 = CambiarPasswordForm()

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
       
        if form.is_valid():
            password = request.POST.get('password')
            usuario = form.save()
            
            messages.success(request, 'El usuario fue actualizado correctamente')
            return redirect('usuario:login')

    else:
        form = UsuarioForm(instance=usuario)

    context = {
        "form": form,
        "form1": form1
    }
    
    context.update(subcategorias(request))
    
    # Renderizar el template con los productos
    return render(request, 'perfil.html', context)

def change_password(request):
    usuario = request.user

    form = UsuarioForm(instance=usuario)
    if request.method == 'POST':
        form1 = CambiarPasswordForm(request.POST)
        if form1.is_valid():
            usuario.set_password(form1.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('usuario:login')
    else:
        form1 = CambiarPasswordForm()

    context = {
        "form": form,
        "form1": form1
    }
    context.update(subcategorias(request))
    
    # Renderizar el template con los productos
    return render(request, 'perfil.html', context)

def subcategorias(request):
    # Obtener todas las subcategorías
    subcategorias = Subcategoria.objects.all()
    # Retornarlas en un diccionario para que estén disponibles en el contexto de todas las plantillas
    return {'subcategorias': subcategorias}
