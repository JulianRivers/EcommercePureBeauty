from django import forms

from django import forms
from .models import (Producto, ProductoSubcategoria, Subcategoria)


class ProductoForm(forms.ModelForm):
    tiene_iva = forms.BooleanField(required=False, label="¿Tiene IVA?")
    
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'descripcion', 'precio_act', 'imagen']

class DescuentoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = ['precio_desc', 'fecha_fin_desc']
        labels = {
            'precio_desc': 'Precio con Descuento',
            'fecha_fin_desc': 'Fecha de Finalización del Descuento',
        }
        widgets = {
            'fecha_fin_desc': forms.DateInput(attrs={'type': 'date'}),
        }
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre']

class ProductoSubcategoriaForm(forms.ModelForm):
    class Meta:
        model = ProductoSubcategoria
        fields = ['subcategoria',]
        labels = {
            'subcategoria': 'Categoria',
            }
        widgets = {
            'subcategoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductoSubcategoriaForm, self).__init__(*args, **kwargs)
        self.fields['subcategoria'].required = False