from django import forms

from django import forms
from .models import (Producto, ProductoSubcategoria, Categoria)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'descripcion', 'precio_act', 'imagen']

class ProductoSubcategoriaForm(forms.ModelForm):
    class Meta:
        model = ProductoSubcategoria
        fields = ['subcategoria',]
        labels = {
            'subcategoria': 'Categoria',
            }
        
class CategoriaPadreForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre',
        }