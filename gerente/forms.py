from django import forms

from .models import (UserProfile, Viatico)

#Formularios

class Login(forms.Form):
    """ Formulario de Login para Gerente y Empleado"""
    email = forms.CharField(label='Email ', required=True)
    password = forms.CharField(label='Contraseña ', widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
     required=True)
