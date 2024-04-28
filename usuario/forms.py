from django import forms

from django import forms
from django.core.exceptions import ValidationError
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


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'apellidos', 'celular', 'email','direccion', 'ciudad']

class CambiarPasswordForm(forms.ModelForm):
    password_confirm = forms.CharField( label="Confirmar Contraseña", max_length=100, widget=forms.PasswordInput(attrs={'placeholder': '•••••••••'}))
    class Meta:
        model = UserProfile
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '••••••••••'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user