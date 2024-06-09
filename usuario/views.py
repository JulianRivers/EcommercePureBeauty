from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib import messages
from django.http import JsonResponse
from .models import (UserProfile, Carrito)
from producto.models import (ProductoEnCarrito, Producto, Subcategoria, ListaDeseo)
from pedido.models import Pedido, DetallePedido, MetodoPago, EstadoPedido
from .forms import (LoginForm, RegistroForm, UsuarioForm, CambiarPasswordForm)
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from decimal import Decimal
from django.utils import timezone



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
    
    # Obtener el usuario actual
    usuario_actual = request.user
    
    # Crear un diccionario para almacenar los estados de la lista de deseos de cada producto
    estado_lista_deseos = {}
    lista = productos_recientes
    # Verificar si el usuario está autenticado
    if usuario_actual.is_authenticated:
        # Obtener todos los productos en la lista de deseos del usuario
        productos_lista_deseos = ListaDeseo.objects.filter(usuario=usuario_actual)    
        estado_lista_deseos = [producto.producto.id for producto in productos_lista_deseos]
        lista = []
        for producto in productos_recientes:
            producto.is_lista = producto.id in estado_lista_deseos
            lista.append(producto)
    # Pasar los productos al contexto del template
    context = {
        'productos_todos': productos_todos,
        'productos_recientes': lista,
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

    usuario_actual = request.user
    is_lista = False
    
    # Verificar si el usuario está autenticado
    if usuario_actual.is_authenticated:
        # Verificar si el producto está en la lista de deseos del usuario
        is_lista = ListaDeseo.objects.filter(usuario=usuario_actual, producto=producto).exists()
    
    # Agregar is_lista al objeto producto
    producto.is_lista = is_lista

    if request.method == 'POST':
        cantidad = request.POST.get('cantidad', None)
        if cantidad is not None:
            carrito, created = Carrito.objects.get_or_create(usuario=usuario_actual)
            try:
                producto_en_carrito = ProductoEnCarrito.objects.get(carrito=carrito, producto=producto)
                producto_en_carrito.cantidad = F('cantidad') + int(cantidad)
                producto_en_carrito.save()
            except ProductoEnCarrito.DoesNotExist:
                ProductoEnCarrito.objects.create(carrito=carrito, producto=producto, cantidad=int(cantidad))

            return redirect('usuario:carrito_compra_cliente')  # Redirigir a la página del perfil del usuario o a donde desees

    context = {
        'producto': producto,
        'cantidades': cantidades,
    }

    return render(request, 'detalle_producto.html', context)



def nuevos(request):
    # Obtener los primeros 8 productos con la fecha de actualización más reciente
    productos_recientes = Producto.objects.filter(is_activo=True).order_by('-ult_actualizacion')[:8]
     # Obtener el usuario actual
    usuario_actual = request.user
    
    # Crear un diccionario para almacenar los estados de la lista de deseos de cada producto
    estado_lista_deseos = {}
    lista = productos_recientes
    # Verificar si el usuario está autenticado
    if usuario_actual.is_authenticated:
        # Obtener todos los productos en la lista de deseos del usuario
        productos_lista_deseos = ListaDeseo.objects.filter(usuario=usuario_actual)    
        estado_lista_deseos = [producto.producto.id for producto in productos_lista_deseos]
        lista = []
        for producto in productos_recientes:
            producto.is_lista = producto.id in estado_lista_deseos
            lista.append(producto)
    # Pasar los productos al contexto del template
    context = {
        'productos_recientes': lista,
    }
    
    context.update(subcategorias(request))
    # Renderizar el template con los productos
    return render(request, 'nuevos.html', context)

def perfil(request):
    usuario = request.user
    form = UsuarioForm(instance=usuario)
    form1 = CambiarPasswordForm()

    # Obtener los pedidos del usuario
    pedidos = Pedido.objects.filter(usuario=usuario).order_by('-fecha')

    context = {
        "form": form,
        "form1": form1,
        "pedidos": pedidos,  # Añadir pedidos al contexto
    }
    
    context.update(subcategorias(request))
    
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

def productos_por_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, pk=subcategoria_id)
    productos = Producto.objects.filter(productosubcategoria__subcategoria=subcategoria)
    usuario_actual = request.user
    
    # Crear un diccionario para almacenar los estados de la lista de deseos de cada producto
    estado_lista_deseos = {}
    lista = productos
    # Verificar si el usuario está autenticado
    if usuario_actual.is_authenticated:
        # Obtener todos los productos en la lista de deseos del usuario
        productos_lista_deseos = ListaDeseo.objects.filter(usuario=usuario_actual)    
        estado_lista_deseos = [producto.producto.id for producto in productos_lista_deseos]
        lista = []
        for producto in productos:
            producto.is_lista = producto.id in estado_lista_deseos
            lista.append(producto)
    context = {
        'subcategoria': subcategoria,
        'productos': lista,
    }
    context.update(subcategorias(request))
    return render(request, 'productos_categorias.html', context)


def agregar_a_lista_deseos(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    usuario = request.user

    # Verificar si el producto ya está en la lista de deseos del usuario
    en_lista_deseos = ListaDeseo.objects.filter(usuario=usuario, producto=producto).exists()

    if en_lista_deseos:
        # Si el producto ya está en la lista de deseos, lo eliminamos
        ListaDeseo.objects.filter(usuario=usuario, producto=producto).delete()
        message = f"{producto.nombre} se ha eliminado de tu lista de deseos."
    else:
        # Si el producto no está en la lista de deseos, lo agregamos
        ListaDeseo.objects.create(usuario=usuario, producto=producto)
        message = f"{producto.nombre} se ha agregado a tu lista de deseos."

    return JsonResponse({'success': True, 'message': message})

def verificar_lista_deseos(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    usuario = request.user
    en_lista_deseos = ListaDeseo.objects.filter(usuario=usuario, producto=producto).exists()
    return JsonResponse({'in_wishlist': en_lista_deseos})


def lista_deseos(request):
    usuario = request.user
    productos_en_lista = ListaDeseo.objects.filter(usuario=usuario).select_related('producto')
    context = {
        'productos_en_lista': productos_en_lista,
    }
    context.update(subcategorias(request))
    
    return render(request, 'lista_deseos.html', context)

def carrito_compra_cliente(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    carrito_items = ProductoEnCarrito.objects.filter(carrito=carrito)
    
    total_pagar = carrito_items.annotate(
        subtotal=ExpressionWrapper(
            F('cantidad') * F('producto__precio_act'),
            output_field=DecimalField()
        )
    ).aggregate(
        total=Sum('subtotal', output_field=DecimalField())
    )['total']
    
    if total_pagar is None:
        total_pagar = Decimal(0)

    context = {
        'carrito_items': carrito_items,
        'total_pagar': total_pagar,
    }
    context.update(subcategorias(request))
    return render(request, 'carrito_compra_cliente.html', context)

def pagar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        # Carrito vacío o no encontrado
        return redirect('carrito_compra_cliente')
    
    carrito_items = ProductoEnCarrito.objects.filter(carrito=carrito)
    if not carrito_items.exists():
        # Sin productos en el carrito
        return redirect('carrito_compra_cliente')
    
    # Crear el pedido
    total_compra = carrito_items.annotate(
        subtotal=ExpressionWrapper(
            F('cantidad') * F('producto__precio_act'),
            output_field=DecimalField()
        )
    ).aggregate(
        total=Sum('subtotal', output_field=DecimalField())
    )['total']

    metodo_pago = MetodoPago.objects.first()  # Suponiendo que tienes métodos de pago predefinidos
    estado_pedido = EstadoPedido.objects.first()  # Suponiendo que tienes estados de pedido predefinidos

    pedido = Pedido.objects.create(
        direccion_entrega=request.user.direccion,
        fecha=timezone.now(),
        total_compra=total_compra,
        usuario=request.user,
        metodo=metodo_pago,
        estado_pedido=estado_pedido,
    )

    for item in carrito_items:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            precio_producto=item.producto.precio_act,
            cantidad=item.cantidad,
        )

    # Limpiar el carrito después de crear el pedido
    carrito_items.delete()
    carrito.delete()

    return redirect('usuario:perfil')  # Redirigir a la página de perfil del usuario
   