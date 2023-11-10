from django.contrib import admin

from .models import (Categoria, Producto, ProductoEnCarrito, ProductoSubcategoria, Subcategoria)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # list_display=('id', 'nombre')
    # list_filter=('nombre',) 
    ordering=('-nombre',)
    search_fields=('nombre',)

@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductoEnCarrito)
class ProductoCarritoAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductoSubcategoria)
class ProductoSubcategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass


