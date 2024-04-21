from django.contrib import admin

from .models import (Producto, ProductoEnCarrito, ProductoSubcategoria, Subcategoria)

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


