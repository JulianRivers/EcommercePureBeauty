from django.shortcuts import (render, redirect, get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse

from gerente.models import (Evento, Viatico)
from .forms import (AgregarViatico, Registro)
# Controladores del empleado

def inicio(request):
    """
    Página de inicio donde el empleado ve todos los eventos a los que está asociado
    name: "empleado:inicio"
    """
    if request.user.is_anonymous:
        return redirect('empleado:registro')
    user = request.user
    eventos = Evento.objects.filter(asistenciaevento__usuario=user)
    context = {
        'eventos': eventos
    }
    return render(request, 'eventos.html', context)

@login_required
def evento(request, idEvento:int):
    """
    Página donde se ven los viaticos en detalle del evento
    name = "empleado:evento"
    """
    evento = get_object_or_404(Evento, id=idEvento)
    viaticos = Viatico.objects.filter(evento=evento)

    context = {
        'evento': evento,
        'viaticos': viaticos
    }
    return render(request, 'eventos-detalle.html', context)

@login_required
def agregarViatico(request, idEvento:int):
    """
    Pagina donde se agrega la información de los viaticos
    name= "empleado:inicio"
    """
    evento = get_object_or_404(Evento, id=idEvento)
    if request.method == 'POST':
        form = AgregarViatico(request.POST, request.FILES)
        if form.is_valid():
            viatico = form.save(commit=False)
            viatico.evento = evento
            viatico.verificado=False
            viatico.save()
            return redirect('empleado:evento', idEvento=evento.id)        
    else:
        form = AgregarViatico()
    context = {
        'form': form,
        'evento': evento,
    }
    return render(request, 'agregar-viatico.html', context)

@csrf_exempt
def mi_vista_ajax(request):
    if request.method == 'POST':
        # Procesa la solicitud AJAX
        # Realiza cualquier operación necesaria en el servidor
        data = {'message': 'Solicitud AJAX recibida correctamente'}
        return JsonResponse(data)

def registerView(request):
    if not request.user.is_anonymous: 
        messages.error(request, "Cierre sesión antes de registrar otro usuario.")
        return redirect('empleado:inicio')
    if request.method == 'POST':
        form = Registro(request.POST)
        if form.is_valid():
            password = request.POST.get('password')  # Recuperar el valor del campo "password"
            usuario = form.save(commit=False)
            usuario.set_password(password)
            usuario.save()
            return redirect('root:login')        
    else:
        form = Registro()
    context = {
        'form': form,
    }
    return render(request, 'registro.html', context)