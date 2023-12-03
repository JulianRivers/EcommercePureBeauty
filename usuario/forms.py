from django import forms

from django import forms
from .models import (UserProfile, Pais, Departamento, Ciudad, )


#Formularios

class LoginForm(forms.Form):
    """ Formulario de Login para Gerente y Empleado"""
    email = forms.CharField(label='Email ', required=True)
    password = forms.CharField(label='Contraseña ', widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
     required=True)


class RegistroForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'apellidos', 'direccion', 'email', 'password', 'celular', 'ciudad']

