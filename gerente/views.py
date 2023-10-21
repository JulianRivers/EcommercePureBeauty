from django.shortcuts import render, redirect
from django.contrib.auth import (login, logout)
from django.contrib import messages

from .models import (UserProfile, Evento)
from .forms import (Login)

#Controladores
def loginView(request):
    """
    root:login Lógica del login
    """
    if request.user.is_superuser:
        return redirect('/admin')
    elif not request.user.is_anonymous: 
        return redirect('empleado:inicio')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = UserProfile.objects.get(email=email)
            if usuario is not None and usuario.check_password(password):
                login(request, usuario)
                return redirect('/admin') if usuario.is_superuser else redirect('empleado:inicio')
            else:
                messages.error(request, "Contraseña incorrecta")
        except Exception as e:
            messages.error( request, "Lo sentimos, no pudimos encontrar tu cuenta")
            usuario = None
            print(e)
    form = Login()
    return render(request, 'login.html', {'form': form})


def index(request):
    """
    root:index
    """
    return render(request, 'index.html')

def logoutView(request):
    logout(request)
    return redirect('root:index')
