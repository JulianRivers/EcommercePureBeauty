from django import forms

from gerente.models import (UserProfile, Viatico)

class Registro(forms.ModelForm):
    """ Formulario de registro para empleados *No se planea usar* """
    class Meta:
        model = UserProfile
        fields = ['name', 'apellidos', 'email', 'departamento', 'password']
        labels = {
            'name': 'Nombres',
            'apellidos': 'Apellidos',
            'email': 'Email ',
            'departamento': 'Departamento',
            'password': 'Contraseña',
        }

class AgregarViatico(forms.ModelForm):
    """ Formulario de empleado donde reporta los gastos en un evento """
    class Meta:
        model = Viatico
        fields = ['fecha_gasto', 'tipo_viatico', 'costo', 'soporte']
        labels ={
            'fecha_gasto': 'Fecha',
            'tipo_viatico': 'Tipo',
            'costo': 'Costo',
            'soporte': 'Soporte',
        }
        widgets = {
            'fecha_gasto': forms.DateInput(attrs={'type': 'date'}),
        }