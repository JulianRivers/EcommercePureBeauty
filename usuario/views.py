from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib import messages

from .models import (UserProfile)
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
    clientes = UserProfile.objects.all()
    
    return render(request, 'clientes.html', {'clientes' : clientes})



